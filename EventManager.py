from PackageEvent import *
class EventManager:
    def __init__(self, tour_global, package_load, location_strings, arrival_times):
        self.events = []
        pickup_arrival_time = arrival_times.pop(0)

        for package in package_load:
            self.events.append(
                PackageEvent(package.id_unique, PackageEventType.pickup, pickup_arrival_time, location_strings[0]))

        for i, destination_index in enumerate(tour_global):
            if destination_index == 0:
                continue

            destination_string = location_strings[destination_index]
            print(f"\t\t\tpackage delivered to index: {destination_index} of address: {destination_string}")

            packages = self.get_packages_with_matching_destination(destination_string, package_load)
            if len(packages) == 0:
                print("zero!")
            for package in packages:
                self.events.append(
                    PackageEvent(package.id_unique, PackageEventType.delivery, arrival_times[i], destination_string))

        # for event in events:
        #    print(f"\t\t\t\tevent: {event}")

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

        # Sort events by time for accurate status determination
        events = self.events
        sorted_events = sorted(events, key=lambda e: e.time)

        for event in sorted_events:
            # If the event is for the given package and occurred before or exactly at the query time
            if event.package_id == package_id and event.time <= query_time:
                # Update the last known status
                last_known_status = event.event_type

        # Check the value of last known status and return the status string
        if last_known_status == PackageEventType.pickup:
            return "Picked up"
        elif last_known_status == PackageEventType.delivery:
            return "Delivered"
        else:
            return "Status unknown"

    def get_packages_with_matching_destination(self, destination_string, package_load):
        packages = []
        for package in package_load:
            address_string = package.get_address_string()
            # print(f"\taddress_string: {address_string} destination_string: {destination_string}")
            if address_string == destination_string:
                packages.append(package)
        return packages
