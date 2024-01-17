# Ashley Tharp AKA Ashley Gelwix ###Student ID: 001251433
# BS Computer Science
# Start Date: Nov 1, 2019
# Program Mentor: Denece Meyer, (385) 428-6184, Mountain Time
# email: athar16@my.wgu.edu, ashley.tharp@gmail.com

import copy
import TimeUtils                                     # authored by student
from CSVParser_Distances import CSVParser_Distances  # authored by student
from CSVParser_Locations import CSVParser_Locations  # authored by student
from TimeUtils import *                              # authored by student
from Location import Location                        # authored by student
from NearestNeighbor import NearestNeighbor          # authored by student
from Driver import Driver                            # authored by student
from PackageManager import PackageManager            # authored by student
from EventManager import EventManager                # authored by student



def init_data(num_drivers):
    """
    Initialize all necessary data structures and objects for the program.

    Parameters:
    - num_drivers (int): Number of drivers to be initialized.

    Returns:
    A tuple containing initialized package manager, adjacency matrix, locations,
    location strings, and drivers.
    """
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
    """
    Initialize drivers for the delivery system.

    Parameters:
    - num_drivers (int): The number of drivers to be initialized.

    Returns:
    A list of Driver objects.
    """
    drivers = []
    for driver_id_num in range(0, num_drivers):
        driver = Driver(driver_id_num, earliest_start_time)
        drivers.append(driver)
    return drivers

if __name__ == '__main__':

    # Initialize various variables and constants for the program
    max_pkg_load_size_per_truck = 16  # Maximum number of packages a truck can hold
    num_trucks = 3  # Total number of trucks
    num_drivers = 2  # Maximum number of drivers
    max_miles = 140  # Maximum miles the two trucks combined can travel
    earliest_start_time = get_time("8:00am")  # Earliest start time for drivers
    avg_speed_mph = 18  # Average speed in miles per hour. Assumes no time for packing/unpacking.
    avg_num_pkgs_per_day = 40  # Average number of packages to deliver each day

    # Initialize data structures
    package_manager, adj_matrix, locations, location_strings, drivers = init_data(num_drivers) # init all data structures
    package_manager_cache = copy.deepcopy(package_manager)
    package_id_cache = package_manager.get_all_package_ids()

    print(f"after init func: {package_manager.how_many_packages()}")

    start_time = earliest_start_time # create earliest start time as time object
    nearest_neighbor_algo = NearestNeighbor(avg_speed_mph) # initialize nearest neighbor implementation

    driver_end_times = [] # when each driver returns to HUB, end of drive time will be timestamped
    drivers = init_drivers(num_drivers) # create drivers

    event_manager = EventManager(package_manager, max_pkg_load_size_per_truck, location_strings, adj_matrix, nearest_neighbor_algo, drivers)

    while True:
        # Main Menu
        print("Choose an option from below or enter 'quit' to exit the program. ")
        print("1: see a package status at a a particular time")
        print("2: see status of all packages at a particular time")
        print("3: total milage and final status of all packages")

        option = input("Enter an option: ")

        # Process user input and provide corresponding functionality
        # Exit the program if 'quit' is entered
        if option.lower() == 'quit':
            break

        # Handle invalid input
        if option.isdigit() == False:
            print("Error: enter a number value for option or 'quit' to exit. Try again.")
            continue

        # Check for valid option range
        if int(option) < 1 or int(option) > 8:
            print("Error: enter a number value for option or 'quit' to exit. Try again.")
            continue

        if option.lower() == 'quit':
                break

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
            package = package_manager_cache.get_package_copy(package_id)
            package.set_delivery_time(status[2])
            package.set_status(status[0])
            print(package)

            # if package_manager_cache.does_package_exist(package_id):
            #     print("boop")
            #     print(package_manager_cache.get_package_copy(package_id))
            # else:
            #     print("OH NO PACKAGE NO EXIST!")


        elif option == "2":
            time = TimeUtils.input_valid_time()
            time_str = TimeUtils.get_time_string(time)
            at_hub, en_route, delivered_with_time = event_manager.get_package_bundles_at_time(time, package_id_cache)
            print(f"at hub: {at_hub}")
            for package_id in at_hub:
                package = package_manager_cache.get_package_copy(package_id)
                print(package)

            print(f"en route: {en_route}")
            for package_id in en_route:
                package = package_manager_cache.get_package_copy(package_id)
                package.set_status("En Route")
                print(package)

            print(f"delivered:")
            for item in delivered_with_time:
                print(f"package id: {item[0]} delivery time: {item[1]} driverID: {item[2]}")
                package = package_manager_cache.get_package_copy(item[0])
                package.set_status("Delivered")
                package.set_delivery_time(item[1])
                print(package)

            print("Driver mileage at time: ")
            for driver in drivers:
                mileage_at_time = driver.get_mileage_at_time(time)
                print(f"\t{time_str} driver: {driver.idNum} mileage: {mileage_at_time}")

        elif option == "3":
            deliveries = event_manager.get_all_delivery_events()
            sorted_deliveries = sorted(deliveries, key=lambda event: int(event.package_id))
            for delivery in sorted_deliveries:
                print(delivery)
                package = package_manager_cache.get_package_copy(delivery.package_id)
                package.set_status("Delivered")
                package.set_delivery_time(TimeUtils.get_time_string(delivery.time))
                print(package)


            print("Driver mileage: ")
            for driver in drivers:
                time = TimeUtils.get_time("11:59pm")
                mileage_at_time = driver.get_mileage_at_time(time)
                print(f"\t driver: {driver.idNum} mileage: {mileage_at_time}")

            event_manager.print_all_events_for_package("25")


    print("Goodbye!")
