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


def init_data(num_drivers):
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

    drivers = init_drivers(num_drivers)

    return my_hash_table, adjacency_matrix, locations, location_strings, drivers

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

    packages_hash_table, adj_matrix, locations, location_strings, drivers = init_data(num_drivers) # init all data structures
    package_manager = PackageManager(packages_hash_table) # init package manager

    start_time = earliest_start_time # create earliest start time as time object
    nearest_neighbor_algo = NearestNeighbor(avg_speed_mph) # initialize nearest neighbor implementation

    driver_end_times = [] # when each driver returns to HUB, end of drive time will be timestamped
    drivers = init_drivers(num_drivers) # create drivers

    event_manager = EventManager(package_manager, max_pkg_load_size_per_truck, location_strings, adj_matrix, nearest_neighbor_algo, drivers)

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
