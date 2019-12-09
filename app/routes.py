""" Creates routes """

from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
import os
import apiclient
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle 
from datetime import datetime, timedelta
import datefinder
import requests

credentials = pickle.load(open("token.pkl", "rb"))
service = apiclient.discovery.build("calendar", "v3", credentials=credentials)

""" Connecting to my calendar """ 
result = service.calendarList().list().execute()
calendar_id = result['items'][0]['id']

""" Making New Event! """

def create_event(start_time_str, summary, duration=1, description=None, location=None):
    matches=list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=duration)
        
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start':{
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/New_York'
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/Chicago'
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},
            ],
        },
        'recurrence': [
            'RRULE:FREQ=WEEKLY',
        ],
    }
    return service.events().insert(calendarId='primary', body=event).execute()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    """ Using LoginForm class, implements the structure of a create account page"""
    form = LoginForm()
    if form.validate_on_submit():
        #flash('Login requested for user {}, remember_me={}'.format(
            #form.username.data, form.remember_me.data))
        return redirect(url_for('survey'))
    return render_template('create_account.html',  title='Create Account', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Using LoginForm class, implements the structure of a log in page """
    form = LoginForm()
    if form.validate_on_submit():
        #flash('Login requested for user {}, remember_me={}'.format(
            #form.username.data, form.remember_me.data))
        return redirect(url_for('calendar'))
    return render_template('login.html',  title='Sign In', form=form)
    
@app.route('/calendar')
def calendar():
    return render_template('calendar.html', title='Calendar')

@app.route('/event')
def event():
    return render_template('event.html', title= 'Events')

@app.route('/task')
def task():
    return render_template('task.html', title= 'Tasks')

@app.route('/survey')
def survey():
    return render_template('survey.html', title='Survey')

@app.route('/newevent', methods=['GET','POST'])
def newevent():
    summary = request.form['eventname']
    day_of_week = request.form['dayofweek']
    start_hour = request.form['shour']
    start_min = request.form['smin']
    am1 = request.form['day1']
    end_hour = request.form['ehour']
    end_min = request.form['emin']
    am2 = request.form['day2']   
    #print("The event name is '" + summary + "'")
    s = day_of_week + start_hour + start_min + am1 
    duration = ""
    if am1 == "am" and am2 == "pm":
        two = int(end_hour) + 12
        duration_hour = two - int(start_hour)
        duration_minute = int(end_min.strip(":")) - int(start_min.strip(":"))
        minutes = duration_minute/60
        duration = duration_hour + minutes
        duration = duration

    elif am1 == "am" and am2 == "am":
        duration_hour = int(end_hour) - int(start_hour)
        duration_minute = int(end_min.strip(":")) - int(start_min.strip(":"))
        minutes = duration_minute/60
        duration = duration_hour + minutes
        duration = duration

    elif am1 == "pm" and am2 == "pm":
        one = int(start_hour) + 12
        two = int(end_hour) + 12
        duration_hour = two - one
        duration_minute = int(end_min.strip(":")) - int(start_min.strip(":"))
        minutes = duration_minute/60
        duration = duration_hour + minutes           
        duration = duration

    elif am1 == "pm" and am2 == "am":
        one = int(end_hour) + 12
        duration_hour = int(end_hour) - one
        duration_minute = int(end_min.strip(":")) - int(start_min.strip(":"))
        minutes = duration_minute/60
        duration = duration_hour + minutes
        duration = duration
       
    create_event(s, summary, duration)
    return redirect('/calendar')

@app.route('/newtask', methods=['GET','POST'])
def newtask():
    title = request.form['taskname']
    due_date= request.form['duedate']
    time_estimate = request.form['timeestimate']
    stress= request.form['stress']
    return redirect('/calendar')