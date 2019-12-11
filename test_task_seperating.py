import json
from datetime import datetime, timedelta
import math
import pickle
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

credentials = pickle.load(open("token.pkl", "rb"))
service = apiclient.discovery.build("calendar", "v3", credentials=credentials)

""" Connecting to my calendar """ 
result = service.calendarList().list().execute()
calendar_id = result['items'][0]['id']

def break_up_tasks():
    
    with open('tasks.json', 'rb') as file:
        task_database = json.load(file)
    
    with open('user_preference.json', 'rb') as file:
        task_database = json.load(file)
        
    unplaced_tasks = {}
    for key in task_database:
        if task_database[key]["is_placed"] == False:
            unplaced_tasks[key] = task_database[key]
    
    order_keys_date = sorted(unplaced_tasks, key=lambda x: unplaced_tasks[x]['due_date'])
    print(order_keys_date)
    date_format = "%Y-%m-%d"

    for key in order_keys_date:
        print(key)
        number_of_chunks = unplaced_tasks[key]["time_est"]
        today = datetime.today()
        due_date = datetime.strptime(unplaced_tasks[key]["due_date"], date_format)
        number_of_days_to_complete = (due_date - today).days
        if number_of_days_to_complete > 0:
            chunks_per_day = math.ceil(float(number_of_chunks)/number_of_days_to_complete)
            for chunk in chunks_per_day:
                page_token = None
                while True:
                    events = service.events().list(calenderId='primary', pageToken=page_token).execute()
                    for event in events['items']:
                        print(event["summary"])
                    page_token = events.get('nextPageToken')
                    if not page_token:
                        break
        else:
            continue



break_up_tasks()