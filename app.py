from flask import Flask
from flask import render_template
import os

schedule_api_consumer_key = 'jLUJW35SkxFhfUHEl8v_8TdsKyAa'
schedule_api_secret_key   = 'tWwcysNIVwVTzi4Gd2AM_54fT4sa'
app = Flask(__name__)

app.secret_key = os.urandom(24)