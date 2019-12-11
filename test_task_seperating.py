import json
from datetime import datetime, timedelta
import math
import pickle
import apiclient
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle 
import json
from datetime import datetime, timedelta
import datefinder

credentials = pickle.load(open("token.pkl", "rb"))
service = apiclient.discovery.build("calendar", "v3", credentials=credentials)

""" Connecting to my calendar """ 
result = service.calendarList().list().execute()
calendar_id = result['items'][0]['id']

def break_up_tasks():
    
    with open('tasks.json', 'rb') as file:
        task_database = json.load(file)
    
    with open('user_preference.json', 'rb') as file:
        user_preferences_database = json.load(file)
    
    start_day_time = int(user_preferences_database["start_day_hour"])
    end_day_time = int(user_preferences_database["end_day_hour"]) + 12
        
    unplaced_tasks = {}
    for key in task_database:
        if task_database[key]["is_placed"] == False:
            unplaced_tasks[key] = task_database[key]
    
    order_keys_date = sorted(unplaced_tasks, key=lambda x: unplaced_tasks[x]['due_date'])
    date_format = "%Y-%m-%d"

    for key in order_keys_date:
        print(key)
        number_of_chunks = unplaced_tasks[key]["time_est"]
        today = datetime.today()
        due_date = datetime.strptime(unplaced_tasks[key]["due_date"], date_format)
        number_of_days_to_complete = (due_date - today).days

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

                    start_date = datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0).isoformat() + 'Z'

                    end_date = datetime(available_days[day].year, available_days[day].month, available_days[day].day, end_day_time, minute, 0).isoformat() + 'Z'
                    events = get_tasks_day(start_date, end_date)
                    if len(events) is not 0:
                        minute = minute + 15
        else:
            continue

def get_tasks_day(start_date, end_date):
    with open('user_preference.json', 'rb') as file:
        user_preferences_database = json.load(file)

    eventsResult = service.events().list(calendarId=calendar_id, timeMin=start_date, timeMax=end_date, singleEvents=True, orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    return events

break_up_tasks()