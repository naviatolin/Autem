""" Calendar functionality """
import numpy as np
import datetime
from datetime import date
from datetime import time

# for later: add all times in datetime time object
# for later: add dates in datetime date object

class Category:
    """
    A type of event or task object
    """
    def __init__(self, name, color):
        """
        Assign a name and a color to a category
        """
        self.name = name
        self.color = color

class Event:
    """
    A scheduled meeting in the user's timeline.
    """
    def __init__(self, start_time, end_time, Category):
        """
        Assigns a start time, end time, and a category to the event.
        """
        self.start_time = start_time
        self.end_time = end_time


class Task:
    """
    An assignment that the user has to complete.
    """
    def __init__(self, start_date, time_duration, end_date, percent, Category):
        """
        Assigns the start date, total estimated time, end date, percent already complete and category to a task.
        """
        self.time_duration = time_duration
        self.start_date = start_date
        self.end_date = due_date

    def break_up_task(self):
        """
        Break up a task into somewhat equal chunks over a few days.
        """
        day_difference = self.end_date - self.start_date
        time_per_day = np.ceil(self.time_duration/day_difference)

        self.broken = []
        for x in range(0,day_difference):
            self.broken.append(Block(time_per_day))

        return self.broken

class Block:
    """
    A chunk of time allocated in the user's timeline.
    """
    def __init__(self, time):
        """
        Initialize a block with the number of minutes per day that the opject takes up.
        """
        # this will take in either a task or an event and create a "block" with dimensions so that we can draw it later
        self.time = time_per_day

    def determine_size(self):
        """
        Find the size of the block.
        """
        hour = 30 # this is in pixels
        conv = np.round(time_per_day/60, 2)
        size = conv/hour 
        pass

    def schedule_it(self):
        """
        TO DO: Schedule the block in the user's day.
        """
        self.start_time = start_time
        self.end_time = end_time

class Day:
    """
    A day in the user's timeline.
    """
    def __init__(self, date):
        """
        Assign a date object to this day class. Create an array that has one entry for every minute in the day.
        """
        self.date = date
        self.things = [] # list of all of the tasks a user has in one day

        self.array = [] #each minute has an entry, boolean for each 
        minutes = []
        for hour in range(0,24):
            for minute in range(0,60):
                minutes.append(False)
            self.array.append(minutes)
        
    def update_day_events(self, Event):
        """
        Update the day's array by switching each minute entry that is occupied to 1.
        """
        event_duration = Event.end_time - Event.start_time

        hour = Event.start_time.hour
        minute = Event.start_time.minute

        inside_duration = True

        while inside_duration:
            self.array[hour][minute] = True

            minute = minute + 1

            if minute > 59:
                minute = 0
                hour = hour + 1

            if hour is Event.end_time.hour and minute is Event.end_time.minute:
                inside_duration = False
        
        self.things.append(Event)

        
    def update_day_tasks(self, Task):
        """
        Update the list of tasks that the day has to complete
        """
        

  
#soft_des = Category("something", "blue")
#get_stuff_done = Task(60, 75, category)

# smallest worktime is 30 minutes
# break between worktimes is 5 minutes
# longest worktime is 3 hours
# 5 minute breaks are 1.2 times
# for every 20 minutes over 5 minutes you add 0.3
# 
