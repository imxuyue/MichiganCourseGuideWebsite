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

    try:
        options['terms'] = get_terms()
    except:
        options['api_error'] = True

 
    options['backpack'] = session['backpack']

    return render_template('index.html', **options)

@app.route('/<term_code>')
def schools(term_code):
    options = {}
    try:
        options['schools'] = get_schools(term_code)
        options['terms'] = get_terms()
        options['TermCode'] = str(term_code)
    except:
        options['api_error'] = True

    return render_template('schools.html', **options)

@app.route('/<term_code>/<schoolcode>')
def subjects(term_code,schoolcode):
    options = {}
    try:
        options['subjects'] = get_subjects(term_code, schoolcode)
        options['SchoolCode'] = schoolcode
        options['schools'] = get_schools(term_code)
        options['terms'] = get_terms()
        options['TermCode'] = str(term_code)
    except:
        options['api_error'] = True

    return render_template('subjects.html', **options)

@app.route('/<term_code>/<schoolcode>/<subjectcode>')
def courses(term_code,schoolcode,subjectcode):
    options = {}
    try:
        options['subjects'] = get_subjects(term_code, schoolcode)
        options['SchoolCode'] = schoolcode
        options['schools'] = get_schools(term_code)
        options['terms'] = get_terms()
        options['TermCode'] = str(term_code)
        options['courses'] = get_courses(term_code, schoolcode, subjectcode)
        options['SubjectCode'] = subjectcode
    except:
        options['api_error'] = True

    return render_template('courses.html', **options)

@app.route('/<term_code>/<schoolcode>/<subjectcode>/<catalognbr>', methods=['GET', 'POST'])
def classinfo(term_code, schoolcode, subjectcode, catalognbr):
    options = {}

    if 'backpack' not in session:
        session['backpack'] = {}
        session['backpack']['items'] = {}
 
    if request.method == 'POST':
        
        session['backpack']['items'][request.form['submitButton']] = {}
        session['backpack']['items'][request.form['submitButton']]['SectionNumber'] = (request.form['SectionNumber'])
        session['backpack']['items'][request.form['submitButton']]['EnrollmentStatus'] = (request.form['EnrollmentStatus'])
        '''
        session['backpack']['items'][request.form['submitButton']]['Times'] = (request.form['Times'])
        '''
        session['backpack']['items'][request.form['submitButton']]['CombinedDays'] = (request.form['CombinedDays'])
        session['backpack']['items'][request.form['submitButton']]['CombinedTimes'] = (request.form['CombinedTimes'])
        session['backpack']['items'][request.form['submitButton']]['MeetingCount'] = (request.form['MeetingCount'])
        session['backpack']['items'][request.form['submitButton']]['AvailableSeats'] = (request.form['AvailableSeats'])
        session['backpack']['items'][request.form['submitButton']]['WaitTotal'] = (request.form['WaitTotal'])

        session['backpack']['path'] = {}
        session['backpack']['path']['Term'] = (request.form['Term'])
        session['backpack']['path']['School'] = (request.form['School'])
        session['backpack']['path']['Subject'] = (request.form['Subject'])
        session['backpack']['path']['Course'] = (request.form['Course'])


        
        '''
        session['backpack'][request.form['submitButton']]['DaysTimes'] = []
    
        counter = 0
        while counter < session['backpack'][request.form['submitButton']]['MeetingCount']:
            temp1 = 'Days' + str(counter)
            session['backpack'][request.form['submitButton']]['DaysTimes'].append(request.form[temp1])
            counter += 1
        '''


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
        
        '''
        options['days'] = 'None'
        for meeting in options['sections']['Meeting']:
            options['days'] += meeting['Days']
            options['Days'] += ' '

        options['Times'] = ''
        for meeting in options['sections']['Meeting']:
            options['Times'] += meeting['Times']
            optinos['Times'] += ' '
        '''
    except:
        options['api_error'] = True

    for section in options['sections']:
        meeting = section['Meeting']
        if type(meeting) is not list:
            temp_list = [ meeting ]
            section['Meeting'] = temp_list
        
        section['CombinedDays'] = ''
        section['MeetingCount'] = 0
        for meeting in section['Meeting']:
            section['CombinedDays'] += str(meeting['Days'])
            section['CombinedDays'] += ' '
            section['MeetingCount'] +=1
        
        section['CombinedTimes'] = ''
        for meeting in section['Meeting']:
            section['CombinedTimes'] += str(meeting['Times'])
            section['CombinedTimes'] += ' '
        
    
    return render_template('details.html', **options)

@app.route('/backpack', methods=['GET', 'POST'])
def backpack():
    options = {}

    if 'backpack' not in session:
        session['backpack'] = {}
        session['backpack']['items'] = {}
    
    if request.method == 'POST':
        del session['backpack']['items'][request.form['param1']]

    try:
        options['terms'] = get_terms()
        options['backpack'] = session['backpack']

    except:
        options['api_error'] = True

    return render_template('backpack.html', **options)







