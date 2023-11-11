from TimeUtils import *

class Driver:
    def __init__(self, idNum, earliest_start_time):
        self.idNum = idNum
        self.start_times = [earliest_start_time]
        self.tours = []

    def add_start_time(self, start_time):
        self.start_times.append(start_time)

    def get_last_start_time(self):
        return self.start_times[-1]

    def __str__(self):
        start_times_str = [get_time_string(time) for time in self.start_times]
        return f'driver id: {self.idNum} start_times: {start_times_str}'

    def add_tour(self, tour_obj):
        self.tours.append(tour_obj)

    def get_mileage_at_time(self, query_time):
        total_mileage = 0
        for tour in self.tours:
            total_mileage += tour.get_mileage_at_time(query_time)
        return total_mileage

    def get_total_mileage(self):
        total_mileage = 0
        for tour in self.tours:
            total_mileage += tour.get_total_mileage()
        return total_mileage
