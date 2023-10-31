# Ashley Tharp AKA Ashley Gelwix ###Student ID: 001251433
# BS Computer Science
# Start Date: Nov 1, 2019
# Program Mentor: Denece Meyer, (385) 428-6184, Mountain Time
# email: athar16@my.wgu.edu, ashley.tharp@gmail.com

import TimeUtils
from CSVParser_Packages import CSVParser_Packages  # authored by student
from CSVParser_Distances import CSVParser_Distances  # authored by student
from CSVParser_Locations import CSVParser_Locations  # authored by student
from EventManager import EventManager  # authored by student
from HashTable import HashTable  # authored by student
from Location import Location  # authored by student
from NearestNeighbor import NearestNeighbor  # authored by student
from Driver import Driver  # authored by student
from PackageManager import PackageManager
from TimeUtils import *  # authored by student


def init_data():
    # init packages
    packages_parser = CSVParser_Packages("packages.csv")
    package_tuples = packages_parser.parse2()  # tuple is: (package_id, package_object)
    my_hash_table = HashTable(len(package_tuples))
    for package_tuple in package_tuples:
        my_hash_table.add(package_tuple[0], package_tuple[1])

    # init locations
    locations_parser = CSVParser_Locations("locations.csv")
    location_strings = locations_parser.get_unique_location_strings()
    num_locations = len(location_strings)
    print(f"num_locations: {num_locations}")
    locations = []
    for i in range(0, len(location_strings)):
        locations.append(Location(i, "", location_strings[i]))

    # init distances
    distances_parser = CSVParser_Distances("distances.csv")
    adjacency_matrix = distances_parser.create_adjacency_matrix(location_strings)

    return my_hash_table, adjacency_matrix, locations, location_strings


def get_submatrix(matrix, start_row, end_row, start_col, end_col):
    return [row[start_col:end_col + 1] for row in matrix[start_row:end_row + 1]]


def extract_submatrix(matrix, indices):
    # print(f"extract_submatrix() indices: {indices}")
    submatrix = []
    for i in indices:
        row = []
        for j in indices:
            # print(f"i: {i} j: {j} matrix_ij: {matrix[i - 1][j - 1]}")
            row.append(matrix[i][j])
        submatrix.append(row)
    return submatrix


def get_indices_for_locations(unique_locations):
    # now get the list of location coordinates that match these addresses in the original adj_matrix
    indices = []
    for unique_location in unique_locations:
        for lstring in location_strings:
            if lstring == unique_location:
                new_index = location_strings.index(unique_location)
                # print(f"adding index {new_index} for location: {unique_location}")
                indices.append(new_index)
    return indices


def get_unique_locations(package_load, location_strings):
    unique_locations = []
    for package in package_load:
        unique_locations.append(package.get_address_string())
    unique_locations = list(set(unique_locations))
    return unique_locations





def init_drivers(num_drivers):
    drivers = []
    for driver_id_num in range(0, num_drivers):
        driver = Driver(driver_id_num, earliest_start_time)
        drivers.append(driver)
    return drivers


if __name__ == '__main__':

    # initialize variables
    max_pkg_load_size_per_truck = 16  # max num packages a truck can hold
    num_trucks = 3   # 3 trucks total
    num_drivers = 2  # two drivers max
    max_miles = 140 # the two trucks combined cannot travel more than 140 miles
    earliest_start_time = get_time("8:00am") # earliest start time
    avg_speed_mph = 18  # avg speed. Packing/unpacking truck takes no time.
    avg_num_pkgs_per_day = 40 # num packages to deliver each day

    packages_hash_table, adj_matrix, locations, location_strings = init_data() # init all data structures
    package_manager = PackageManager(packages_hash_table) # init package manager

    start_time = earliest_start_time # create earliest start time as time object
    nearest_neighbor_algo = NearestNeighbor(avg_speed_mph) # initialize nearest neighbor implementation

    driver_end_times = [] # when each driver returns to HUB, end of drive time will be timestamped
    drivers = init_drivers(num_drivers) # create drivers
    event_manager = EventManager() # create event manager

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
            load_size = min(max_pkg_load_size_per_truck, how_many_packages) # decide whether to get 16 or all remaining
            package_load = package_manager.get_packages(load_size)  # get load of determined size
            new_pickup_time = driver.get_last_start_time()          # new pickup time is the beginning of the next drive session

            new_pickup_time_str = TimeUtils.get_time_string(new_pickup_time) # new pickup time as string
            print(f"\tdriver {driver.idNum} got: {len(package_load)} packages at: {new_pickup_time_str}")

            # for package in package_load:
            #    print(f"package: {package}")

            # some packages may go to same place, determine the total set of locations for our trip
            unique_locations = get_unique_locations(package_load, location_strings)

            # now get the list of location coordinates that match these addresses in the original adj_matrix
            indices = get_indices_for_locations(unique_locations)
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

            #print(f"\t\ttour: {tour_global} tour length: {len(tour)}")
            #print(f"\t\ttour_cost: {tour_cost} tour_cost length: {len(tour_cost)}")
            #print(f"\t\ttotal_cost: {total_cost}")
            #print(f"\t\tarrival_times_str: {arrival_times_str} len: {len(arrival_times_str)}")

            # for each hop in a tour we will create an event.
            event_manager.add_tour(tour_global, package_load, location_strings, arrival_times)

    event_manager.print_all_events()

    while True:
        # Get packageID from the user
        package_id = input("Enter the packageID (or 'quit' to exit): ")

        # Exit condition
        if package_id.lower() == 'quit':
            break

        # Get time from the user
        time = TimeUtils.input_valid_time()
        time_str = TimeUtils.get_time_string(time)
        status = event_manager.get_package_status_at_time(package_id, time)

        # Now you can process or store the packageID and time as required
        print(f"package: {package_id} at time: {time_str} is: {status}")

        event_manager.print_all_events_for_package(package_id)

    print("Goodbye!.")
