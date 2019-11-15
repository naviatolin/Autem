import numpy as np
import datetime
from datetime import date
from datetime import time

# all times in datetime time object
# add dates in datetime date object
class Category:
    def __init__(self, name, color):
        self.name = name
        self.color = color

class Event:
    def __init__(self, start_time, end_time, Category):
        self.start_time = start_time
        self.end_time = end_time


class Task:
    def __init__(self, start_date, time_duration, end_date, percent, Category):
        self.time_duration = time_duration
        self.start_date = start_date
        self.end_date = due_date

    def break_up_task(self):
        """
        Break up a task into somewhat equal chunks over a few days.

        Arguments:
            Task : class object
        """
        day_difference = self.end_date - self.start_date
        time_per_day = np.ceil(self.time_duration/day_difference)

        self.broken = []
        for x in range(0,day_difference):
            self.broken.append(Block(time_per_day))

        return self.broken

class Block:
    def __init__(self, time):
        # this will take in either a task or an event and create a "block" with dimensions so that we can draw it later
        self.time = time_per_day

    def determine_size(self):
        hour = 30 # this is in pixels
        conv = np.round(time_per_day/60, 2)
        size = conv/hour 
        pass

    def schedule_it(self):
        self.start_time = start_time
        self.end_time = end_time

class Day:
    def __init__(self, date):
        self.date = date
        self.things = []

        self.array = []
        minutes = []
        for hour in range(0,24):
            for minute in range(0,60):
                minutes.append(0)
            self.array.append(minutes)
        
    def update_day_events(self, Event):
        event_duration = Event.end_time - Event.start_time

        hour = Event.start_time.hour
        minute = Event.start_time.minute

        inside_duration = True

        while inside_duration:
            self.array[hour][minute] = 1

            minute = minute + 1

            if minute > 59:
                minute = 0
                hour = hour + 1

            if hour is Event.end_time.hour and minute is Event.end_time.minute:
                inside_duration = False
        
        self.things.append(Event)

        
    def update_day_tasks(self, Task):
        pass

  
soft_des = Category("something", "blue")
get_shit_done = Task(60, 75, category)
# smallest worktime is 30 minutes
# break between worktimes is 5 minutes
# longest worktime is 3 hours
# 5 minute breaks are 1.2 times
# for every 20 minutes over 5 minutes you add 0.3
# 
