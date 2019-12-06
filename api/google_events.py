from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle 
from datetime import datetime, timedelta
import datefinder
import requests
#scopes = ['https://www.googleapis.com/auth/calendar']

credentials = pickle.load(open("token.pkl", "rb"))
service = build("calendar", "v3", credentials=credentials)

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
            'timeZone': 'America/Chicago'
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

#create_event("3 december 1 am", "sleeping", 3, "this is the time where I sleep", "BOSTON")