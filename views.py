from flask import render_template, request, url_for, session, redirect
from app import app
from schedule_api import get_terms, get_schools, get_subjects, get_courses, get_courseDescr, get_sections
import json, types

@app.route('/')
def index():
    options = {}

    if 'backpack' not in session:
        session['backpack'] = {}
        session['backpack']['items'] = {}
        session['backpack']['path'] = {}

    try:
        options['terms'] = get_terms()
    except:
        options['api_error'] = True

    return render_template('index.html', **options)

@app.route('/<term_code>')
def schools(term_code):
    options = {}

    if 'backpack' not in session:
        session['backpack'] = {}
        session['backpack']['items'] = {}
        session['backpack']['path'] = {}

    try:
        options['schools'] = get_schools(term_code)
        options['terms'] = get_terms()
        options['TermCode'] = str(term_code)
        options['backpack'] = session['backpack']['items']
    except:
        options['api_error'] = True

    return render_template('schools.html', **options)

@app.route('/<term_code>/<schoolcode>')
def subjects(term_code,schoolcode):
    options = {}
    if 'backpack' not in session:
        session['backpack'] = {}
        session['backpack']['items'] = {}
        session['backpack']['path'] = {}

    try:
        options['subjects'] = get_subjects(term_code, schoolcode)
        options['SchoolCode'] = schoolcode
        options['schools'] = get_schools(term_code)
        options['terms'] = get_terms()
        options['TermCode'] = str(term_code)
        options['backpack'] = session['backpack']['items']
    except:
        options['api_error'] = True

    return render_template('subjects.html', **options)

@app.route('/<term_code>/<schoolcode>/<subjectcode>')
def courses(term_code,schoolcode,subjectcode):
    options = {}
    
    if 'backpack' not in session:
        session['backpack'] = {}
        session['backpack']['items'] = {}
        session['backpack']['path'] = {}

    try:
        options['subjects'] = get_subjects(term_code, schoolcode)
        options['SchoolCode'] = schoolcode
        options['schools'] = get_schools(term_code)
        options['terms'] = get_terms()
        options['TermCode'] = str(term_code)
        options['courses'] = get_courses(term_code, schoolcode, subjectcode)
        options['SubjectCode'] = subjectcode
        options['backpack'] = session['backpack']['items']
    except:
        options['api_error'] = True

    return render_template('courses.html', **options)

@app.route('/<term_code>/<schoolcode>/<subjectcode>/<catalognbr>', methods=['GET', 'POST'])
def classinfo(term_code, schoolcode, subjectcode, catalognbr):
    options = {}

    if 'backpack' not in session:
        session['backpack'] = {}
        session['backpack']['items'] = {}
        session['backpack']['path'] = {}
 
    if request.method == 'POST':
        
        session['backpack']['items'][request.form['submitButton']] = {}
        session['backpack']['items'][request.form['submitButton']]['SubjectCode'] = (request.form['SubjectCode'])
        session['backpack']['items'][request.form['submitButton']]['CatalogNumber'] = (request.form['CatalogNumber'])
        session['backpack']['items'][request.form['submitButton']]['SectionNumber'] = (request.form['SectionNumber'])
        session['backpack']['items'][request.form['submitButton']]['SectionType'] = (request.form['SectionType'])
        session['backpack']['items'][request.form['submitButton']]['EnrollmentStatus'] = (request.form['EnrollmentStatus'])
        session['backpack']['items'][request.form['submitButton']]['CombinedDays'] = (request.form['CombinedDays'])
        session['backpack']['items'][request.form['submitButton']]['CombinedTimes'] = (request.form['CombinedTimes'])
        session['backpack']['items'][request.form['submitButton']]['CombinedDaysTimes'] = (request.form['CombinedDaysTimes'])
        session['backpack']['items'][request.form['submitButton']]['MeetingCount'] = (request.form['MeetingCount'])
        session['backpack']['items'][request.form['submitButton']]['AvailableSeats'] = (request.form['AvailableSeats'])
        session['backpack']['items'][request.form['submitButton']]['WaitTotal'] = (request.form['WaitTotal'])
        session['backpack']['items'][request.form['submitButton']]['InstrName'] = (request.form['InstrName'])

        session['backpack']['path'] = {}
        session['backpack']['path']['Term'] = (request.form['Term'])
        session['backpack']['path']['School'] = (request.form['School'])
        session['backpack']['path']['Subject'] = (request.form['Subject'])
        session['backpack']['path']['Course'] = (request.form['Course'])



        return redirect ("/backpack")

    try:
        options['SchoolCode'] = schoolcode
        options['schools'] = get_schools(term_code)
        options['terms'] = get_terms()
        options['TermCode'] = str(term_code)
        options['subjects'] = get_subjects(term_code, schoolcode)
        options['SubjectCode'] = subjectcode
        options['courses'] = get_courses(term_code, schoolcode, subjectcode)
        options['CatalogNumber'] = str(catalognbr)
        options['CourseDescr'] = get_courseDescr(term_code, schoolcode, subjectcode, catalognbr)
        options['sections'] = get_sections(term_code, schoolcode, subjectcode, catalognbr)
        options['backpack'] = session['backpack']['items']
        
    except:
        options['api_error'] = True

    for section in options['sections']:
        
        if 'Meeting' not in section:
            section['Meeting'] = {'Days': 'TBA', 'Times': 'TBA'}
        meeting = section['Meeting']
        if type(meeting) is not list:
            temp_list = [ meeting ]
            section['Meeting'] = temp_list


        if 'ClassInstructors' not in section:
            section['ClassInstructors'] = {'InstrName': 'TBA'}
        instructor = section['ClassInstructors']
        if type(instructor) is not list:
            temp_list2 = [ instructor ]
            section["ClassInstructors"] = temp_list2

        section['CombinedInstructors'] = ''
        for instructor in section['ClassInstructors']:
            section['CombinedInstructors'] += str(instructor['InstrName'])
            section['CombinedInstructors'] += ' '
        
        section['CombinedDaysTimes'] = ''
        section['MeetingCount'] = 0
        for meeting in section['Meeting']:
            section['CombinedDaysTimes'] += str(meeting['Days'])
            section['CombinedDaysTimes'] += ' '
            section['CombinedDaysTimes'] += str(meeting['Times'])
            section['CombinedDaysTimes'] += '  '
            section['MeetingCount'] +=1
        
    
    return render_template('details.html', **options)

@app.route('/backpack', methods=['GET', 'POST'])
def backpack():
    options = {}

    if 'backpack' not in session:
        session['backpack'] = {}
        session['backpack']['items'] = {}
        session['backpack']['path'] = {}
    
    if request.method == 'POST':
        del session['backpack']['items'][request.form['param1']]

    try:
        options['terms'] = get_terms()
        options['backpack'] = session['backpack']

    except:
        options['api_error'] = True

    return render_template('backpack.html', **options)







