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

""" Our algorithm that gets tasks, breaks them up, and schedules them """
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
        chunks_left = 0 # reset the amount of chunks that are can't be scheduled on a day
        number_of_chunks = unplaced_tasks[key]["time_est"]
        today = datetime.today()
        due_date = datetime.strptime(unplaced_tasks[key]["due_date"], date_format)
        number_of_days_to_complete = (due_date - today).days
        task_database[key]["is_placed"] = True
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
                                create_event(datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0), unplaced_tasks[key]["task_summary"])

                                create_rest_event(datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time + 1, minute, 0), 'Destress If Possible")
                                break
                            
                            if start_day_time + 1 == end_day_time:
                                chunks_left = chunks_left + 1

                    else:
                        start_date_string = datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0).isoformat()
                        create_event(datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0), unplaced_tasks[key]["task_summary"])

                        create_rest_event(datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time + 1, minute, 0), 'Destress If Possible")
                    
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
                                        create_event(datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0), unplaced_tasks[key]["task_summary"])

                                        create_rest_event(datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time + 1, minute, 0), 'Destress If Possible")
                                        break
                                    
                                    if start_day_time + 1 == end_day_time:
                                        chunks_left = chunks_left + 1

                            else:
                                start_date_string = datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0).isoformat()
                                create_event(datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time, minute, 0), unplaced_tasks[key]["task_summary"])

                                create_rest_event(datetime(available_days[day].year, available_days[day].month, available_days[day].day, start_day_time + 1, minute, 0), 'Destress If Possible")
                    
        else:
            continue

def get_tasks_hour(start_date, end_date):
    with open('user_preference.json', 'rb') as file:
        user_preferences_database = json.load(file)
    
    eventsResult = service.events().list(calendarId=calendar_id, timeMin=start_date, timeMax=end_date, singleEvents=True, orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    return events

def create_task_chunk(start_time, summary, description=None, location=None):
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

break_up_tasks()
# date = datetime(2019)