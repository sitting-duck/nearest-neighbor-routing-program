from datetime import datetime
from enum import Enum

import TimeUtils


class PackageEventType(Enum):
    pickup = 0
    delivery = 1
class PackageEvent():

    def __init__(self, package_id, event_type, time, address):
        self.package_id = package_id
        self.event_type = event_type
        self.time = time
        self.address = address

    def __str__(self):
        """
            Returns a string representation of the Location object.
            :return: A string representing the Package object.
        """
        time_str = TimeUtils.get_time_string(self.time)
        return f'package_id: {self.package_id} event_type: {self.event_type} time: {time_str}\n'

    def __repr__(self):
        """
            Returns a string representation of the Location object.
            :return: A string representing the Package object.
        """
        return self.__str__()