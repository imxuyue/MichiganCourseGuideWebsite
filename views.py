from flask import render_template, request, url_for, session
from app import app
from schedule_api import get_terms, get_schools, get_subjects, get_courses, get_course_descr, get_sections
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

@app.route('/terms/<term_code>')

def schools(term_code):
    options = {}
    try:
        options['schools'] = get_schools(term_code)
        options['terms'] = get_terms()
        options['TermCode'] = str(term_code)
    except:
        options['api_error'] = True

    return render_template('schools.html', **options)

@app.route('/terms/<term_code>/schools/<school_code>')

def subjects(term_code,school_code):
    options = {}
    try:
        options['subjects'] = get_subjects(term_code, school_code)
        options['SchoolCode'] = school_code
        options['schools'] = get_schools(term_code)
        options['terms'] = get_terms()
        options['TermCode'] = str(term_code)
    except:
        options['api_error'] = True

    return render_template('subjects.html', **options)

@app.route('/terms/<term_code>/schools/<school_code>/subjects/<subject_code>')

def courses(term_code,school_code,subject_code):
    options = {}
    try:
        options['subjects'] = get_subjects(term_code, school_code)
        options['SchoolCode'] = school_code
        options['schools'] = get_schools(term_code)
        options['terms'] = get_terms()
        options['TermCode'] = str(term_code)
        options['courses'] = get_courses(term_code, school_code, subject_code)
        options['SubjectCode'] = str(subject_code)
    except:
        options['api_error'] = True

    return render_template('courses.html', **options)

@app.route('/terms/<term_code>/schools/<school_code>/subjects/<subject_code>/courses/<course_code>', methods=['GET', 'POST'])

def course_info(term_code, school_code, subject_code, course_code):
    options = {}

    if 'backpack' not in session:
        session['backpack'] = {}
 
    if request.method == 'POST':
        session['backpack'][request.form['submitButton']] = []
        session['backpack'][request.form['submitButton']].append(request.form['param1'])
        session['backpack'][request.form['submitButton']].append(request.form['param2'])
    
    try:

        options['SchoolCode'] = school_code
        options['schools'] = get_schools(term_code)
        options['terms'] = get_terms()
        options['TermCode'] = str(term_code)
        options['subjects'] = get_subjects(term_code, school_code)
        options['SubjectCode'] = str(subject_code)
        options['courses'] = get_courses(term_code, school_code, subject_code)
        options['CourseCode'] = str(course_code)
        options['course_descr'] = get_course_descr(term_code, school_code, subject_code, course_code)
        options['sections'] = get_sections(term_code, school_code, subject_code, course_code)
   
    except:
        options['api_error'] = True

    return render_template('courseinfo.html', **options)


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


@app.route('/fave_colors')
def staff_fave_colors():
    options = {'staff': ['Adam', 'Tim', 'Grace', 'Maxim', 'Ryan']}
    return render_template('fave_colors.html', **options)
 
 
def get_persons_fave_color(person):
    '''
    This is obviosly a silly example, but in your code,
    your would probably be calling a schedule_api function.
    '''
    if person == 'Adam':
        return 'green'
    elif person == 'Tim':
        return 'blue'
    elif person == 'Grace':
        return 'orange'
    elif person == 'Maxim':
        return 'yellow'
    elif person == 'Ryan':
        return ''
 
@app.route('/get_fave_color')
def get_fave_color():
    if 'person' in request.args:
        return json.dumps(get_persons_fave_color(request.args.get('person')))
    else:
        return json.dumps('unknown person')
'''
@app.route('/terms/<term_code>/<school_code>')

def courses(term_code,school_code):
    options = {}
    try:
        options['schools'] = get_schools(term_code)
        options['terms'] = get_terms()
        options['TermCode'] = str(term_code)
    except:
        options['api_error'] = True

    return render_template('schools.html', **options)

'''