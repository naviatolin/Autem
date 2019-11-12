import numpy as np
import datetime
from datetime import date

class Category:
    def __init__(self, name, color):
        self.name = name
        self.color = color

class Event:
    def __init__(self, start_time, end_time, Category):
        self.start_time = start_time
        self.end_time = end_time


class Task:
    def __init__(self, time_duration, percent, Category):
        self.time_duration = time_duration
        self.start_date = date.today()
        print(self.start_date)

    def break_up_task(self):
        """
        Break up a task into somewhat equal chunks over a few days.

        Arguments:
            Task : class object
        """
        pass

class Block:
    def __init__(self):
        # this will take in either a task or an event and create a "block" with dimensions so that we can draw it later
        pass

    def determine_size(self):
        pass


category = Category("something", "blue")
get_shit_done = Task(60, 75, category)
# smallest worktime is 30 minutes
# break between worktimes is 5 minutes
# longest worktime is 3 hours
# 5 minute breaks are 1.2 times
# for every 20 minutes over 5 minutes you add 0.3
# 
