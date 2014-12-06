from flask import render_template, request, url_for
from app import app
from schedule_api import get_terms, get_schools, get_subjects, get_courses

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

@app.route('/terms/<term_code>/<schoolcode>')
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

@app.route('/terms/<term_code>/<schoolcode>/<subjectcode>')
def courses(term_code, schoolcode, subjectcode):
    options = {}
    try:
        options['courses'] = get_courses(term_code, schoolcode, subjectcode)
        options['SubjectCode'] = subjectcode
        options['subjects'] = get_subjects(term_code, schoolcode)
        options['SchoolCode'] = schoolcode
        options['schools'] = get_schools(term_code)
        options['terms'] = get_terms()
        options['TermCode'] = str(term_code)
    except:
        options['api_error'] = True

    return render_template('courses.html', **options)
