# Ashley Tharp AKA Ashley Gelwix ###Student ID: 001251433
# BS Computer Science
# Start Date: Nov 1, 2019
# Program Mentor: Denece Meyer, (385) 428-6184, Mountain Time
# email: athar16@my.wgu.edu, ashley.tharp@gmail.com
import TimeUtils
from CSVParser_Packages import CSVParser_Packages  # authored by student
from CSVParser_Distances import CSVParser_Distances  # authored by student
from CSVParser_Locations import CSVParser_Locations  # authored by student
from EventManager import EventManager
from HashTable import HashTable  # authored by student
from Location import Location  # authored by student
from NearestNeighbor import NearestNeighbor  # authored by student
from Driver import Driver  # authored by student

from PackageEvent import PackageEventType, PackageEvent
from TimeUtils import *


def InitData():
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


def get_sub_matrix_for_packages(adj_matrix, packages):
    pass
    # address_strings = []
    # for package in packages:
    #     address_strings.append(package.get_address_string())

    # unique_address_list = list(set(address_strings)) # use set to create a list of only the unique addresses

    # locations = []
    # for i in range(num_locations-1):
    #     new_location = Location(location_strings[i])
    #     #print(f"new_location: {new_location}")
    #     #     for j in range(num_locations-1):
    #         address = location_strings[j]
    #         #print(f"to_location: {address}")
    #         distance = adjacency_matrix[i][j]
    #         #print(f"distance: {distance}")
    #         new_location.add_distance(address, distance)
    #     locations.append(new_location)


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


def get_arrival_times(hop_times, start_time):
    arrival_times = [start_time]
    for hop_time in hop_times:
        delta = timedelta(hours=hop_time)
        new_time = arrival_times[-1] + delta
        # print(f"hop_time: {hop_time} delta: {delta} new_time: {get_time_string(new_time)}")
        arrival_times.append(new_time)

    arrival_times_str = [get_time_string(time) for time in arrival_times]
    # arrival_times_str = arrival_times_str[1:]
    return arrival_times, arrival_times_str


def get_drivers(num_drivers):
    drivers = []
    for driver_id_num in range(0, num_drivers):
        driver = Driver(driver_id_num, earliest_start_time)
        drivers.append(driver)
    return drivers


if __name__ == '__main__':
    max_pkg_load_size_per_truck = 16  # max num packages a truck can hold
    num_trucks = 3
    num_drivers = 2
    max_miles = 140
    earliest_start_time = get_time("8:00am")
    avg_speed_mph = 18
    avg_num_pkgs_per_day = 40

    packages_hash_table, adj_matrix, locations, location_strings = InitData()

    start_time = earliest_start_time
    nearest_neighbor_algo = NearestNeighbor(avg_speed_mph)

    driver_end_times = []
    drivers = get_drivers(num_drivers)

    while packages_hash_table.how_many_packages() > 0:

        # sort drivers by last start time
        drivers = sorted(drivers, key=lambda driver: driver.get_last_start_time())
        print("\ndrivers sorted by HUB arrival time: ", end='')
        for driver in drivers:
            print(driver.__str__(), end=' ')
        print()

        for driver in drivers:

            # check if there are any more packages
            how_many_packages = int(packages_hash_table.how_many_packages())
            if how_many_packages == 0:
                break

            # if there are still some, get next batch of packages
            package_load = packages_hash_table.get_n_packages(min(max_pkg_load_size_per_truck, how_many_packages))
            new_pickup_time = driver.get_last_start_time()
            new_pickup_time_str = TimeUtils.get_time_string(new_pickup_time)
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

            arrival_times, arrival_times_str = get_arrival_times(hop_times, new_pickup_time)

            driver.add_start_time(arrival_times[-1])  # the hub arrival time is the last arrival time of the tour

            print(f"\t\ttour: {tour_global} tour length: {len(tour)}")
            print(f"\t\ttour_cost: {tour_cost} tour_cost length: {len(tour_cost)}")
            print(f"\t\ttotal_cost: {total_cost}")
            print(f"\t\tarrival_times_str: {arrival_times_str} len: {len(arrival_times_str)}")

            event_manager = EventManager(tour_global, package_load, location_strings, arrival_times)

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

            print("Goodbye!.")
