from TimeUtils import *


class Driver:
    """
    A class representing a driver in a delivery system.

    Attributes:
    - idNum (int): The unique identifier for the driver.
    - start_times (list): A list of start times for the driver's tours.
    - tours (list): A list of tours assigned to the driver.
    """
    def __init__(self, idNum, earliest_start_time):
        """
        Initialize a Driver object with a unique ID and an earliest start time.

        Parameters:
        - idNum (int): The unique identifier for the driver.
        - earliest_start_time (datetime): The earliest time the driver can start their tour.
        """
        self.idNum = idNum
        self.start_times = [earliest_start_time]
        self.tours = []

    def add_start_time(self, start_time):
        """
        Add a start time to the driver's list of start times.

        Parameters:
        - start_time (datetime): The start time to be added.
        """
        self.start_times.append(start_time)

    def get_last_start_time(self):
        """
        Get the last start time from the driver's list of start times.

        Returns:
        - datetime: The last start time.
        """
        return self.start_times[-1]

    def __str__(self):
        """
        Return a string representation of the Driver object.

        Returns:
        - str: A string representing the driver's ID and start times.
        """
        start_times_str = [get_time_string(time) for time in self.start_times]
        return f'driver id: {self.idNum} start_times: {start_times_str}'

    def add_tour(self, tour_obj):
        """
        Add a tour to the driver's list of tours.

        Parameters:
        - tour_obj: The tour object to be added.
        """
        self.tours.append(tour_obj)

    def get_mileage_at_time(self, query_time):
        """
        Calculate the total mileage driven by the driver up to a specific time.

        Parameters:
        - query_time (datetime): The time at which the mileage is to be calculated.

        Returns:
        - float: The total mileage driven up to the specified time.
        """
        total_mileage = 0
        for tour in self.tours:
            total_mileage += tour.get_mileage_at_time(query_time)
        return total_mileage

    def get_total_mileage(self):
        """
        Calculate the total mileage driven by the driver across all tours.

        Returns:
        - float: The total mileage driven across all tours.
        """
        total_mileage = 0
        for tour in self.tours:
            total_mileage += tour.get_total_mileage()
        return total_mileage
