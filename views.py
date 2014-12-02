from flask import render_template, request
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

@app.route('/win15')
def win15():
    options = {}
    try:
        options['schools'] = get_schools(2020)
    except:
        options['api_error'] = True

    return render_template('win15.html', **options)
