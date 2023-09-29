from TimeUtils import *

class Driver:
    def __init__(self, idNum, earliest_start_time):
        self.idNum = idNum
        self.start_times = [earliest_start_time]

    def add_start_time(self, start_time):
        self.start_times.append(start_time)

    def get_last_start_time(self):
        return self.start_times[-1]

    def __str__(self):
        start_times_str = [get_time_string(time) for time in self.start_times]
        return f'driver id: {self.idNum} start_times: {start_times_str}'