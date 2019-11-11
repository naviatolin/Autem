import numpy as np
import datetime

class Category:
    def __init__(self, name, color):
        self.name = name
        self.color = color

class Event:
    def __init__(self, start_time, end_time, Category):
        self.start_time = start_time
        self.end_time = end_time


class Task:
    def __init__(self, start_date, time_duration, percent, Category):
        self.time_duration = time_duration

def break_up_tasks(Task):
    """
    Break up a task into somewhat equal chunks over a few days.

    Arguments:
        Task : class object
    """
    

# smallest worktime is 30 minutes
# break between worktimes is 5 minutes
# longest worktime is 3 hours
# 5 minute breaks are 1.2 times
# for every 20 minutes over 5 minutes you add 0.3
# 
