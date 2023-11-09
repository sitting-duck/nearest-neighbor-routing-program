from enum import Enum
import TimeUtils

class PackageEventType(Enum):
    pickup = 0
    delivery = 1
class PackageEvent():

    def __init__(self, package_id, event_type, time, address, driver_id):
        self.package_id = package_id
        self.event_type = event_type
        self.time = time
        self.address = address
        self.driver_id = driver_id

    def __str__(self):
        """
            Returns a string representation of the Location object.
            :return: A string representing the Package object.
        """
        time_str = TimeUtils.get_time_string(self.time)
        event_type_str = "Unknown"
        if self.event_type == PackageEventType.pickup:
            event_type_str = "pickup"
        elif self.event_type == PackageEventType.delivery:
            event_type_str = "delivery"

        return f'package_id: {self.package_id} event_type: {event_type_str} time: {time_str} driverID: {self.driver_id}'

    def __repr__(self):
        """
            Returns a string representation of the Location object.
            :return: A string representing the Package object.
        """
        return self.__str__()