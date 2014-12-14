from flask import render_template, request, url_for, session, redirect
from app import app
from schedule_api import get_terms, get_schools, get_subjects, get_courses, get_courseDescr, get_sections
import json, types

@app.route('/')
def index():
    options = {}

    if 'backpack' not in session:
        session['backpack'] = {}

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
 
    if request.method == 'POST':
        session['backpack'][request.form['submitButton']] = []
        session['backpack'][request.form['submitButton']].append(request.form['SectionNumber'])
        session['backpack'][request.form['submitButton']].append(request.form['EnrollmentStatus'])
        session['backpack'][request.form['submitButton']].append(request.form['Days'])
        session['backpack'][request.form['submitButton']].append(request.form['Times'])

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
   
    except:
        options['api_error'] = True

    return render_template('details.html', **options)

@app.route('/backpack', methods=['GET', 'POST'])
def backpack():
    options = {}

    if 'backpack' not in session:
        session['backpack'] = {}
    
    if request.method == 'POST':
        del session['backpack'][request.form['param1']]

    try:
        options['terms'] = get_terms()
        options['backpack'] = session['backpack']

    except:
        options['api_error'] = True

    return render_template('backpack.html', **options)







