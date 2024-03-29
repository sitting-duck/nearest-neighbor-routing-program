from PackageEvent import *
from MatrixUtils import *
from Tour import Tour


class EventManager:
    """
    Class responsible for managing and orchestrating package delivery events.
    This includes planning tours for drivers, tracking package pick-ups and deliveries,
    and managing the overall event timeline.
    """

    def __init__(self, package_manager, max_pkg_load_size_per_truck, location_strings, adj_matrix,
                 nearest_neighbor_algo, drivers):
        """
       Initialize an instance of the EventManager class.

       The EventManager class is responsible for managing and storing events. Picking up a package is an event, and
       dropping off a package is an event. All events are timestamped.

       Attributes:
       - events (list): A list to store events associated with the EventManager instance.
       """
        self.events = []
        self.drivers = drivers
        self.package_manager = package_manager

        while package_manager.how_many_packages() > 0:  # continue processing until all packages are processed

            # sort drivers by last start time
            drivers = sorted(drivers, key=lambda driver: driver.get_last_start_time())

            print("\ndrivers sorted by HUB arrival time: ", end='')
            for driver in drivers:
                print(driver.__str__(), end=' ')
            print()

            # get a new batch of packages to drivers in the order they arrive
            for driver in drivers:

                # check if there are any more packages
                how_many_packages = int(package_manager.how_many_packages())
                if how_many_packages == 0:
                    break

                # if there are still some, get next batch of packages
                load_size = min(max_pkg_load_size_per_truck,
                                how_many_packages)  # decide whether to get 16 or all remaining
                package_load = package_manager.get_packages(load_size)  # get load of determined size

                new_pickup_time = driver.get_last_start_time()  # new pickup time is the beginning of the next drive session

                new_pickup_time_str = TimeUtils.get_time_string(new_pickup_time)  # new pickup time as string
                print(f"\tdriver {driver.idNum} got: {len(package_load)} packages at: {new_pickup_time_str}")

                # some packages may go to same place, determine the total set of locations for our trip
                unique_locations = package_manager.get_unique_locations(package_load, location_strings)

                # now get the list of location coordinates that match these addresses in the original adj_matrix
                indices = get_indices_for_locations(unique_locations, location_strings)
                indices.insert(0, 0)  # HUB will always be a destination

                # create a sub matrix of distances for all the locations needed for this batch of packages
                sub_matrix = extract_submatrix(adj_matrix, indices)
                tour, total_cost, hop_times, tour_cost = nearest_neighbor_algo.run(
                    sub_matrix)  # calculate the tour using the sub matrix

                tour_global = []
                for hop in tour:
                    tour_global.append(indices[hop])

                # each arrival at each location now has an arrival time, these are in order chronologically
                arrival_times, arrival_times_str = TimeUtils.get_arrival_times(hop_times, new_pickup_time)

                driver.add_start_time(arrival_times[-1])  # the hub arrival time is the last arrival time of the tour

                tour_obj = Tour(tour, hop_times, total_cost, tour_cost, new_pickup_time)
                driver.add_tour(tour_obj)

                # print(f"\t\ttour: {tour_global} tour length: {len(tour)}")
                # print(f"\t\ttour_cost: {tour_cost} tour_cost length: {len(tour_cost)}")
                # print(f"\t\ttotal_cost: {total_cost}")
                # print(f"\t\tarrival_times_str: {arrival_times_str} len: {len(arrival_times_str)}")

                # for each hop in a tour we will create an event.
                self.add_tour(tour_global, package_load, location_strings, arrival_times, driver.idNum)

    def add_tour(self, tour_global, package_load, location_strings, arrival_times, driver_id):
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
                PackageEvent(package.id_unique, PackageEventType.pickup, pickup_arrival_time, location_strings[0],
                             driver_id))

        for i, destination_index in enumerate(tour_global):
            if destination_index == 0:
                continue

            destination_string = location_strings[destination_index]
            # print(f"\t\t\tpackage {package.id_unique} delivered to index: {destination_index} of address: {destination_string}")

            packages = self.get_packages_with_matching_destination(destination_string, package_load)

            for package in packages:
                self.events.append(
                    PackageEvent(package.id_unique, PackageEventType.delivery, arrival_times[i], destination_string,
                                 driver_id))

    def get_all_events_up_to_time(self, query_time):
        """
        Retrieve all events that have occurred up to a specific time.

        Parameters:
        - query_time (datetime): The time up to which events are to be retrieved.

        Returns:
        - list: A list of events that occurred up to the specified time.
        """
        # Sort events by time for accurate status determination
        events = self.events
        sorted_events = sorted(events, key=lambda e: e.time)

        events_before_time = [event for event in sorted_events if event.time <= query_time]
        return events_before_time

    def get_package_bundles_at_time(self, query_time, package_id_cache):
        """
        Determine the status of a specific package at a given time.

        Parameters:
        - package_id (int): The ID of the package.
        - query_time (datetime): The time at which the status is to be determined.

        Returns:
        - str: The status of the package at the specified time.
        """
        at_hub = []
        en_route = []
        delivered_with_time = []

        for package_id in package_id_cache:
            status, driver_id, event_time = self.get_package_status_at_time(package_id, query_time)
            if status == "At the HUB":
                at_hub.append(package_id)
            elif status == "En Route":
                en_route.append(package_id)
            elif status.startswith("Delivered"):
                delivered_with_time.append((package_id, event_time, driver_id))

        sorted_delivered_with_time = sorted(delivered_with_time, key=lambda x: int(x[0]))
        return at_hub, en_route, sorted_delivered_with_time

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

        driver_id = -1
        for event in sorted_events:
            # If the event is for the given package and occurred before or exactly at the query time
            if event.package_id == package_id and event.time <= query_time:
                # Update the last known status
                last_known_status = event.event_type
                last_known_time = TimeUtils.get_time_string(event.time)
                driver_id = event.driver_id

        if query_time < TimeUtils.get_time("8:00am"):
            return "At the HUB", driver_id

        # Check the value of last known status and return the status string
        if last_known_status == PackageEventType.pickup:
            return "En Route", driver_id, last_known_time
        elif last_known_status == PackageEventType.delivery:
            return f"Delivered at {last_known_time}", driver_id, last_known_time
        else:
            return "At the HUB", driver_id, last_known_time

    @staticmethod
    def get_packages_with_matching_destination(destination_string, package_load):
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

    def get_all_events(self):
        """
        Retrieve all events.

        Returns:
        - list: A list of all events.
        """
        return self.events

    def get_all_pickup_events(self):
        """
        Retrieve all pickup events.

        Returns:
        - list: A list of all pickup events.
        """
        pickups = []
        for event in self.events:
            if event.event_type == PackageEventType.pickup:
                pickups.append(event)
        return pickups

    def get_times_hub_was_visited(self):
        """
        Retrieve the times when the hub was visited.

        Returns:
        - list: A list of times when the hub was visited.
        """
        times = set()
        pickups = self.get_all_pickup_events()
        for pickup in pickups:
            if pickup.time not in times:
                times.add(TimeUtils.get_time_string(pickup.time))
        return times

    def get_all_delivery_events(self):
        """
        Retrieve all delivery events.

        Returns:
        - list: A list of all delivery events.
        """
        deliveries = []
        for event in self.events:
            if event.event_type == PackageEventType.delivery:
                deliveries.append(event)
        return deliveries

    def print_all_events_for_package(self, package_id):
        """
        Print all events associated with a specific package ID.

        This function filters and prints only the events that are related to the given package ID.

        Parameters:
        - package_id (str): The ID of the package whose events are to be printed.
        """
        for event in self.events:
            if event.package_id == package_id:
                print(f"\t\t\t\tevent: {event}")

    def get_all_events_in_timeframe(self, begin_time, end_time):
        """
        Retrieve all events that occurred within a specified timeframe.

        Parameters:
        - begin_time (datetime): The start time of the timeframe.
        - end_time (datetime): The end time of the timeframe.

        Returns:
        - list: A list of events that occurred within the specified timeframe.
        """
        in_timeframe = []
        for event in self.events:
            if begin_time <= event.time <= end_time:
                in_timeframe.append(event)
        return in_timeframe
