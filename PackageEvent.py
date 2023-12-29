from enum import Enum
import TimeUtils

class PackageEventType(Enum):
    """
    An enumeration representing the types of events that can happen to a package.

    Attributes:
    - pickup (int): Represents a package pickup event.
    - delivery (int): Represents a package delivery event.
    """
    pickup = 0
    delivery = 1
class PackageEvent():
    """
    A class representing an event related to a package in a delivery system.

    Attributes:
    - package_id (str): The unique identifier of the package.
    - event_type (PackageEventType): The type of the event (pickup/delivery).
    - time (datetime): The time at which the event occurred.
    - address (str): The address associated with the event.
    - driver_id (int): The identifier of the driver involved in the event.
    """

    def __init__(self, package_id, event_type, time, address, driver_id):
        """
        Initialize a PackageEvent object with package details and event information.

        Parameters:
        - package_id (str): The unique identifier of the package.
        - event_type (PackageEventType): The type of the event (pickup or delivery).
        - time (datetime): The time at which the event occurred.
        - address (str): The address associated with the event.
        - driver_id (int): The identifier of the driver involved in the event.
        """
        self.package_id = package_id
        self.event_type = event_type
        self.time = time
        self.address = address
        self.driver_id = driver_id

    def __str__(self):
        """
        Returns a string representation of the PackageEvent object.

        Returns:
        - str: A string representing the event with package ID, event type, time, and driver ID.
        """
        time_str = TimeUtils.get_time_string(self.time)
        event_type_str = "Unknown"
        if self.event_type == PackageEventType.pickup:
            event_type_str = "pickup"
        elif self.event_type == PackageEventType.delivery:
            event_type_str = "delivery"

        #return f'package_id: {self.package_id} event_type: {event_type_str} time: {time_str} driverID: {self.driver_id}'
        return f'{event_type_str} for package {self.package_id} at {time_str} by driver: {self.driver_id}'

    def __repr__(self):
        """
        Returns a string representation of the PackageEvent object, ideal for debugging and logging.

        Returns:
        - str: A string representing the event.
        """
        return self.__str__()
