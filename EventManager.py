import TimeUtils
from PackageEvent import *
class EventManager:

    def __init__(self):
        """
       Initialize an instance of the EventManager class.

       The EventManager class is responsible for managing and storing events.

       Attributes:
       - events (list): A list to store events associated with the EventManager instance.
       """
        self.events = []

    def create_events(self, package_manager, ):
        pass
    def add_tour(self, tour_global, package_load, location_strings, arrival_times):
        """
        Initialize an object with events based on packages and their respective delivery locations and times.

        The function captures both pickup and delivery events for packages. A pickup event is added for each package at the start,
        followed by delivery events based on the provided tour sequence (`tour_global`).

        Parameters:
        - tour_global (list): A list of indices representing the sequence of locations to be visited.
        - package_load (list): A list of package objects to be delivered.
        - location_strings (list): A list of strings where each string is an address corresponding to an index in `tour_global`.
        - arrival_times (list): A list of datetime objects representing the arrival times at the respective locations in `tour_global`.

        Attributes:
        - events (list): A list to store PackageEvent objects representing pickup and delivery events.

        Note:
        It's assumed that the package object has an attribute 'id_unique' representing its unique identifier.
        The `get_packages_with_matching_destination` method is used to retrieve packages for a specific destination.
        """
        pickup_arrival_time = arrival_times.pop(0)

        for package in package_load:
            self.events.append(
                PackageEvent(package.id_unique, PackageEventType.pickup, pickup_arrival_time, location_strings[0]))

        for i, destination_index in enumerate(tour_global):
            if destination_index == 0:
                continue

            destination_string = location_strings[destination_index]
            #print(f"\t\t\tpackage {package.id_unique} delivered to index: {destination_index} of address: {destination_string}")

            packages = self.get_packages_with_matching_destination(destination_string, package_load)

            for package in packages:
                self.events.append(
                    PackageEvent(package.id_unique, PackageEventType.delivery, arrival_times[i], destination_string))

    def get_package_status_at_time(self, package_id, query_time):
        """
        Determine the status of a package based on the provided events up to a certain time.

        Parameters:
        - events (list): A list of PackageEvent objects.
        - package_id (int): The ID of the package whose status is to be determined.
        - query_time (datetime): The time at which the package's status is to be checked.

        Returns:
        - str: The status of the package at the given time.
        """

        # Initialize the last known status as None
        last_known_status = None
        last_known_time = None

        # Sort events by time for accurate status determination
        events = self.events
        sorted_events = sorted(events, key=lambda e: e.time)

        for event in sorted_events:
            # If the event is for the given package and occurred before or exactly at the query time
            if event.package_id == package_id and event.time <= query_time:
                # Update the last known status
                last_known_status = event.event_type
                last_known_time = TimeUtils.get_time_string(event.time)

        if query_time < TimeUtils.get_time("8:00am"):
            return "At the HUB"

        # Check the value of last known status and return the status string
        if last_known_status == PackageEventType.pickup:
            return "En Route"
        elif last_known_status == PackageEventType.delivery:
            return f"Delivered at {last_known_time}"
        else:
            return "Unknown"

    def get_packages_with_matching_destination(self, destination_string, package_load):
        """
            Retrieve packages from the provided package load whose destination matches the given destination string.

            Parameters:
            - destination_string (str): The destination string (address) to match against.
            - package_load (list): A list of package objects to search through.

            Returns:
            - list: A list of packages from the package_load that have a destination matching the provided destination_string.

            Note:
            It's assumed that the package object has a method get_address_string() that returns the destination (address) of the package as a string.
            """
        packages = []
        for package in package_load:
            address_string = package.get_address_string()
            # print(f"\taddress_string: {address_string} destination_string: {destination_string}")
            if address_string == destination_string:
                packages.append(package)
        return packages

    def print_all_events(self):
        """
        Print all events managed by this EventManager instance.

        This function iterates through all events stored in the 'events' attribute and prints them.
        """
        for event in self.events:
            print(f"\t\t\t\tevent: {event}")

    def print_all_events_for_package(self, package_id):
        """
        Print all events associated with a specific package ID.

        This function filters and prints only the events that are related to the given package ID.

        Parameters:
        - package_id (int or str): The ID of the package whose events are to be printed.
        """
        for event in self.events:
            if event.package_id == package_id:
                print(f"\t\t\t\tevent: {event}")

