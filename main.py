# Ashley Tharp AKA Ashley Gelwix ###Student ID: 001251433
# BS Computer Science
# Start Date: Nov 1, 2019
# Program Mentor: Denece Meyer, (385) 428-6184, Mountain Time
# email: athar16@my.wgu.edu, ashley.tharp@gmail.com

from CSVParser_Packages import CSVParser_Packages # authored by student
from CSVParser_Distances import CSVParser_Distances # authored by student
from CSVParser_Locations import CSVParser_Locations # authored by student
from HashTable import HashTable # authored by student
from Location import Location # authored by student
from NearestNeighbor import NearestNeighbor # authored by student
from datetime import datetime

def InitData():

    # init packages
    packages_parser = CSVParser_Packages("packages.csv")
    package_tuples = packages_parser.parse2() # tuple is: (package_id, package_object)
    my_hash_table = HashTable(len(package_tuples))
    for package_tuple in package_tuples:
        my_hash_table.add(package_tuple[0], package_tuple[1])

    # init locations
    locations_parser = CSVParser_Locations("locations.csv")
    location_strings = locations_parser.get_unique_location_strings()
    num_locations = len(location_strings)


    # init distances
    distances_parser = CSVParser_Distances("distances.csv")
    adjacency_matrix = distances_parser.create_adjacency_matrix(location_strings)

    return my_hash_table, adjacency_matrix, location_strings

def get_sub_matrix_for_packages(adj_matrix, packages):
    pass
    # address_strings = []
    # for package in packages:
    #     address_strings.append(package.get_address_string())

    #unique_address_list = list(set(address_strings)) # use set to create a list of only the unique addresses

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

def get_time(str):
    """
    str: a string in the format: "9:00am", "5:30pm" etc. Use civilian time and am/pm, not military time.
    Once you have datetime objects, you can easily compare them using standard comparison operators (<, >, ==, etc.).
    """
    time_format = "%I:%M%p"
    time = datetime.strptime(str, time_format)
    return time

def get_submatrix(matrix, start_row, end_row, start_col, end_col):
    return [row[start_col:end_col+1] for row in matrix[start_row:end_row+1]]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    max_pkg_load_size_per_truck = 16  # max num packages a truck can hold
    num_trucks = 3
    num_drivers = 2
    max_miles = 140
    earliest_start_time = get_time("8:00am")
    avg_speed_mph = 18
    avg_num_pkgs_per_day = 40


    packages_hash_table, adj_matrix, location_strings = InitData()

    #print(f"before: {packages_hash_table.how_many_packages()}")
    package_load = packages_hash_table.get_n_packages(max_pkg_load_size_per_truck)
    unique_locations = []
    for package in package_load:
        unique_locations.append(package[0][1].get_address_string())
    unique_locations = list(set(unique_locations))

    print(f'package_load len: {len(package_load)}')
    print(f'unique_location len: {len(unique_locations)}')

    # now get the list of location coordinates that match these addresses in the original adj_matrix
    indices = []
    for unique_location in unique_locations:
        for lstring in location_strings:
            if lstring == unique_location:
                indices.append(location_strings.index(unique_location))
    print(f"le indices: {len(indices)}")


    nearest_neighbor_algo = NearestNeighbor(avg_speed_mph)

    #sub_adjacency_matrix = get_sub_matrix_for_packages(adj_matrix, packages)

    tour, total_cost, time_traveled = nearest_neighbor_algo.run(adj_matrix)

    print(f"tour: {tour} tour length: {len(tour)}")
    print(f"total_cost: {total_cost}")
    print(f"time_traveled: {time_traveled} time_traveled_len: {len(time_traveled)}")



