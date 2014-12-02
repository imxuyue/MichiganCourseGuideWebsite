from flask import render_template, request, url_for
from app import app
from schedule_api import get_terms, get_schools

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