""" Creates routes """

from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, TaskForm, EventForm, SurveyForm
import os
import apiclient
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle 
import json
from datetime import datetime, timedelta
import datefinder
import requests
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import math

credentials = pickle.load(open("token.pkl", "rb"))
service = apiclient.discovery.build("calendar", "v3", credentials=credentials)

""" Connecting to my calendar """ 
result = service.calendarList().list().execute()
calendar_id = result['items'][0]['id']

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

@app.route('/event', methods=['GET', 'POST'])
def event():
    form = EventForm()
    #print(due_date)
    if form.validate_on_submit():
        summary = request.form['eventname']
        day_of_week = request.form['dayofweek']
        start_hour = request.form['shour']
        start_min = request.form['smin']
        am1 = request.form['day1']
        end_hour = request.form['ehour']
        end_min = request.form['emin']
        am2 = request.form['day2'] 

        #print(summary, day_of_week, start_hour, start_min, am1)
        
        s = day_of_week + start_hour + start_min + am1 
        duration = ""
        if am1 == "am" and am2 == "pm":
            two = int(end_hour) + 12
            duration_hour = two - int(start_hour)
            duration_minute = int(end_min.strip(":")) - int(start_min.strip(":"))
            minutes = duration_minute/60
            duration = duration_hour + minutes
            duration = duration - 1

        elif am1 == "am" and am2 == "am":
            duration_hour = int(end_hour) - int(start_hour)
            duration_minute = int(end_min.strip(":")) - int(start_min.strip(":"))
            minutes = duration_minute/60
            duration = duration_hour + minutes
            duration = duration - 1

        elif am1 == "pm" and am2 == "pm":
            one = int(start_hour) + 12
            two = int(end_hour) + 12
            duration_hour = two - one
            duration_minute = int(end_min.strip(":")) - int(start_min.strip(":"))
            minutes = duration_minute/60
            duration = duration_hour + minutes           
            duration = duration - 1

        elif am1 == "pm" and am2 == "am":
            one = int(end_hour) + 12
            duration_hour = int(end_hour) - one
            duration_minute = int(end_min.strip(":")) - int(start_min.strip(":"))
            minutes = duration_minute/60
            duration = duration_hour + minutes
            duration = duration - 1
        
        create_event(s, summary, duration)
        return redirect(url_for('calendar'))
    return render_template('event.html', title= 'Events', form=form)
    

@app.route('/task', methods=['GET', 'POST'])
def task():
    form = TaskForm()
    if form.validate_on_submit():
        task_summary = request.form['title']
        due_date = request.form['due_date']
        time_est = request.form['time_est']
        stress = request.form['stress']
        is_placed = False

        with open('tasks.json', 'rb') as file:
            task_database = json.load(file)    

        task = {'task_summary' : task_summary,
                    'due_date' : due_date, 
                    'time_est': time_est,
                    'stress' : stress,
                    'is_placed' : is_placed}
        index = task_summary.strip()
        index = task_summary.replace(" ", "")
        index = index + str(due_date) + str(time_est)
        task_database[index] = task
                                                    
        with open('tasks.json', 'w') as f:
            json.dump(task_database, f)
        
        break_up_tasks()

        return redirect(url_for('calendar'))
    return render_template('task.html', title= 'Tasks', form=form)

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    form = SurveyForm()
    if form.validate_on_submit():
        one = request.form['level_one']
        two = request.form['level_two']
        three = request.form['level_three']
        start = request.form['start_day_hour']
        end = request.form['end_day_hour']
        lunch = request.form['lunch_hour']
        dinner = request.form['dinner_hour']

        user_info = {'level_one' : one,
                    'level_two' : two,
                    'level_three' : three}
        user_preference = {'start_day_hour' : start,
                            'end_day_hour' : end,
                            'lunch_hour' : lunch,
                            'dinner_hour' : dinner}
        with open('user_info.json', 'w') as f:
            json.dump(user_info, f)
        with open('user_preference.json', 'w') as f:
            json.dump(user_preference, f)
        create_event(lunch, 'lunch', 1)
        create_event(dinner, 'dinner', 1)
        return redirect(url_for('calendar'))    
    return render_template('survey.html', title='Survey', form=form)

def create_event(start_time_str, summary, duration=1, description=None, location=None):
    """ 
    Making New Event! 
    """
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
            'timeZone': 'America/New_York'
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
    print(event)

def get_tasks_hour(start_date, end_date):
    """
    Checks the hour of the task to see if something else is already scheduling
    """
    with open('user_preference.json', 'rb') as file:
        user_preferences_database = json.load(file)
    
    eventsResult = service.events().list(calendarId=calendar_id, timeMin=start_date, timeMax=end_date, singleEvents=True, orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    return events

def create_task_chunk(start_time, summary, description=None, location=None):
    """
    Putting the task chunks into your calendar
    """
    end_time = start_time + timedelta(hours=1)  
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S")
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start':{
            'dateTime': start_time,
            'timeZone': 'America/New_York'
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/New_York'
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    return service.events().insert(calendarId='primary', body=event).execute()

def create_rest_event(start_time, summary, description=None, location=None):
    """
    Scheduling in mental health time!
    """
    end_time = start_time + timedelta(minutes=15)  
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S")
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start':{
            'dateTime': start_time,
            'timeZone': 'America/New_York'
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/New_York'
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    return service.events().insert(calendarId='primary', body=event).execute()

def break_up_tasks():
    """
    Break up the tasks and set the google calendar events so that nothing collides.
    """
    # open the task database
    with open('tasks.json', 'rb') as file:
        task_database = json.load(file)
    
    # open the user preferences database
    with open('user_preference.json', 'rb') as file:
        user_preferences_database = json.load(file)
    
    # when the user wants to start and end working
    start_day_time = int(user_preferences_database["start_day_hour"])
    end_day_time = int(user_preferences_database["end_day_hour"]) + 12
        
    # find which tasks have not been already put in the calendar
    unplaced_tasks = {}
    for key in task_database:
        if task_database[key]["is_placed"] == False:
            unplaced_tasks[key] = task_database[key]
    
    # order these tasks by date
    order_keys_date = sorted(unplaced_tasks, key=lambda x: unplaced_tasks[x]['due_date'])
    date_format = "%Y-%m-%d"

    # check the tasks that haven't been placed in the date ordered way
    for key in order_keys_date:
        chunks_left = 0 # reset the amount of chunks that are can't be scheduled on a day
        number_of_chunks = unplaced_tasks[key]["time_est"] # chunk the task up into 1 hour chunk

        
        today = datetime.today()
        due_date = datetime.strptime(unplaced_tasks[key]["due_date"], date_format)
        number_of_days_to_complete = (due_date - today).days
        task_database[key]["is_placed"] = True
        
        # place the chunks in the calender if it is free
        if number_of_days_to_complete > 0:
            chunks_per_day = math.ceil(float(number_of_chunks)/number_of_days_to_complete)

            available_days = []
            current_day = datetime.today() + timedelta(days=1)
            for day in range(0, number_of_days_to_complete):
                available_days.append(current_day)
                current_day = current_day+ timedelta(days=1)
            

            for day in range(0, len(available_days)):
                for chunk in range(0, chunks_per_day):
                    minute = 0

                    start_date = datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0).isoformat()+ '-05:00'

                    end_date = datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time + 1, minute, 0).isoformat() + '-05:00'

                    events = get_tasks_hour(start_date, end_date)
                    print(events)
                    if len(events) is not 0:
                        while start_day_time + 1 <= end_day_time:
                            minute = minute + 15
                            if minute >= 60:
                                start_day_time = start_day_time + 1
                                minute = minute % 60

                            print(minute)
                            start_date = datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0).isoformat() + '-05:00'
                            print(start_date)

                            end_date = datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time + 1, minute, 0).isoformat() + '-05:00'
                            
                            events = get_tasks_hour(start_date, end_date)
                            print(events)


                            if len(events) is 0:
                                start_date_string = datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0).isoformat()
                                create_task_chunk(datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0), unplaced_tasks[key]["task_summary"])

                                create_rest_event(datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time + 1, minute, 0), "Destress If Possible")
                                break
                            
                            if start_day_time + 1 == end_day_time:
                                chunks_left = chunks_left + 1

                    else:
                        start_date_string = datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0).isoformat()
                        create_task_chunk(datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0), unplaced_tasks[key]["task_summary"])

                        create_rest_event(datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time + 1, minute, 0), "Destress If Possible")

            # if any chunks weren't able to placed try to place them in other available days
            if chunks_left > 0:
                for chunks in range(0, chunks_left):
                    for day in range(0, len(available_days)):
                        for chunk in range(0, chunks_per_day):
                            minute = 0

                            start_date = datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0).isoformat() + '-05:00'

                            end_date = datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time + 1, minute, 0).isoformat() + '-05:00'

                            events = get_tasks_hour(start_date, end_date)
                            print(events)

                            if len(events) is not 0:
                                while start_day_time + 1 <= end_day_time:
                                    minute = minute + 15
                                    if minute >= 60:
                                        start_day_time = start_day_time + 1
                                        minute = minute % 60

                                    start_date = datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0).isoformat() + '-05:00'
                                    print(start_date)

                                    end_date = datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time + 1, minute, 0).isoformat() + '-05:00'
                                    
                                    events = get_tasks_hour(start_date, end_date)
                                    print(events)


                                    if len(events) is 0:
                                        start_date_string = datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0).isoformat()
                                        create_task_chunk(datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0), unplaced_tasks[key]["task_summary"])

                                        create_rest_event(datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time + 1, minute, 0), "Destress If Possible")
                                        break
                                    
                                    if start_day_time + 1 == end_day_time:
                                        chunks_left = chunks_left + 1

                            else:
                                start_date_string = datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0).isoformat()
                                create_task_chunk(datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0), unplaced_tasks[key]["task_summary"])

                                create_rest_event(datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time + 1, minute, 0), "Destress If Possible")
                    
        else:
            continue
        
        
        