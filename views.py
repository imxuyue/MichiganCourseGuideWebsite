from flask import render_template, request, url_for
from app import app
from schedule_api import get_terms, get_schools, get_subjects, get_courses, get_course_descr, get_sections

@app.route('/')
def index():
    options = {}
    try:
        options['terms'] = get_terms()
    except:
        options['api_error'] = True

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

@app.route('/terms/<term_code>/schools/<school_code>/subjects/<subject_code>/courses/<course_code>')

def course_info(term_code, school_code, subject_code, course_code):
    options = {}
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


@app.route('/backpack')
def backpack():
    options = {}
    try:
        options['terms'] = get_terms()
    except:
        options['api_error'] = True

    return render_template('index.html', **options)
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