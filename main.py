# Ashley Tharp AKA Ashley Gelwix ###Student ID: 001251433
# BS Computer Science
# Start Date: Nov 1, 2019
# Program Mentor: Denece Meyer, (385) 428-6184, Mountain Time
# email: athar16@my.wgu.edu, ashley.tharp@gmail.com

import TimeUtils

from CSVParser_Distances import CSVParser_Distances  # authored by student
from CSVParser_Locations import CSVParser_Locations  # authored by student
from TimeUtils import *  # authored by student

from Location import Location  # authored by student
from NearestNeighbor import NearestNeighbor  # authored by student
from Driver import Driver  # authored by student

from PackageManager import PackageManager
from TestPackageManager import TestPackageManager

from EventManager import EventManager  # authored by student
from TestEventManager import TestEventManager # authored by student



def init_data(num_drivers):
    # init packages
    package_manager = PackageManager()  # init package manager

    print(f"In init func: {package_manager.how_many_packages()}")

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

    return package_manager, adjacency_matrix, locations, location_strings, drivers

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

    package_manager, adj_matrix, locations, location_strings, drivers = init_data(num_drivers) # init all data structures
    package_id_cache = package_manager.get_all_package_ids()

    print(f"after init func: {package_manager.how_many_packages()}")

    start_time = earliest_start_time # create earliest start time as time object
    nearest_neighbor_algo = NearestNeighbor(avg_speed_mph) # initialize nearest neighbor implementation

    driver_end_times = [] # when each driver returns to HUB, end of drive time will be timestamped
    drivers = init_drivers(num_drivers) # create drivers

    event_manager = EventManager(package_manager, max_pkg_load_size_per_truck, location_strings, adj_matrix, nearest_neighbor_algo, drivers)
    #event_test_manager = TestEventManager(event_manager, package_manager)

    #event_manager.print_all_events()

    while True:
        # Get packageID from the user
        print("Choose an option from below or enter 'quit' to exit the program. ")
        print("1: see a package status at a a particular time")
        print("2: see all events within a certain time range")
        print("3: see all pickup events")
        print("4: see all delivery events")
        print("5: see status of all packages at a particular time")
        print("6: see all times HUB was visited")
        print("7: print all events")

        option = input("Enter an option: ")

        # Exit condition
        if option.lower() == 'quit':
            break
        if option.isdigit() == False:
            print("Error: enter a number value for option or 'quit' to exit. Try again.")
            continue

        if option == "1":
            package_id = input("Enter the packageID (or 'quit' to exit): ")
            if package_id.isdigit() == False:
                print("Error: package id must be all digits and represent a package that exists. Try again.")
                continue
            if package_id.lower() == 'quit':
                break

            if package_id not in package_id_cache:
                print(f"Error: Package with id: {package_id} does not exist. Try again.")
                print(f"available package ids: {package_id_cache}")
                continue

            # Get time from the user
            time = TimeUtils.input_valid_time()
            time_str = TimeUtils.get_time_string(time)
            status = event_manager.get_package_status_at_time(package_id, time)

            # Now you can process or store the packageID and time as required
            print(f"package: {package_id} at time: {time_str} is: {status}")
            event_manager.print_all_events_for_package(package_id)
        elif option == "2":
            start_time = input_valid_time()
            end_time = input_valid_time()
            events_in_time_frame = event_manager.get_all_events_in_timeframe(start_time, end_time)
            for event in events_in_time_frame:
                print(f"event: {event}")
        elif option == "3":
            pickups = event_manager.get_all_pickup_events()
            for event in pickups:
                print(f"event: {event}")
        elif option == "4":
            deliveries = event_manager.get_all_delivery_events()
            for event in deliveries:
                print(f"event: {event}")
        elif option == "5":
            time = TimeUtils.input_valid_time()
            time_str = TimeUtils.get_time_string(time)
            for package_id in package_id_cache:
                status = event_manager.get_package_status_at_time(package_id, time)
                print(f"{time_str} package: {package_id} status: {status}")

            print("Driver mileage at time: ")
            for driver in drivers:
                mileage_at_time = driver.get_mileage_at_time(time)
                print(f"\t{time_str} driver: {driver.idNum} mileage: {mileage_at_time}"
                      )
        elif option == "6":
            times = event_manager.get_times_hub_was_visited()
            print(times)
        elif option == "7":
            event_manager.print_all_events()


    print("Goodbye!")
