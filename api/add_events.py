""" Making New Event! """
import datefinder
def create_event(start_time_str, summary, duration=1, description=None, location=None):
    matches=list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + datefinder.timedelta(hours=duration)
        
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