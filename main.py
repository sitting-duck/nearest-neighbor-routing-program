from CSVParser_Packages import CSVParser_Packages # authored by student
from CSVParser_Distances import CSVParser_Distances # authored by student
from CSVParser_Locations import CSVParser_Locations # authored by student
from HashTable import HashTable # authored by student
from Location import Location # authored by student
from NearestNeighbor import NearestNeighbor # authored by student
from datetime import datetime

def InitData():
    packages_parser = CSVParser_Packages("packages.csv")
    package_tuples = packages_parser.parse()
    my_hash_table = HashTable(len(package_tuples))
    for myTuple in package_tuples:
        my_hash_table.add(myTuple[0], myTuple[1:])

    distances_parser = CSVParser_Distances("distances.csv")
    locations_parser = CSVParser_Locations("locations.csv")
    location_strings = locations_parser.get_unique_location_strings()

    num_locations = len(location_strings)
    print(f"num_locations: {num_locations}")


    adjacency_matrix = distances_parser.create_adjacency_matrix(location_strings)

    for row in adjacency_matrix:
        print(row)

    locations = []
    for i in range(num_locations-1):
        new_location = Location(location_strings[i])
        print(f"new_location: {new_location}")

        for j in range(num_locations-1):
            address = location_strings[j]
            print(f"to_location: {address}")
            distance = adjacency_matrix[i][j]
            print(f"distance: {distance}")
            new_location.add_distance(address, distance)

        locations.append(new_location)

    for location in locations:
        print(f"location: {location}")


    return my_hash_table, adjacency_matrix


def get_time(str):
    """
    str: a string in the format: "9:00am", "5:30pm" etc. Use civilian time and am/pm, not military time.
    Once you have datetime objects, you can easily compare them using standard comparison operators (<, >, ==, etc.).
    """
    time_format = "%I:%M%p"
    time = datetime.strptime(str, time_format)
    return time


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    max_load_size = 16  # num packages a truck can hold
    num_trucks = 3
    num_drivers = 2
    max_miles = 140
    earliest_start_time = get_time("8:00am")
    avg_speed_mph = 18

    hash_table, adj_matrix = InitData()
    nearest_neighbor_algo = NearestNeighbor()
    tour, total_cost = nearest_neighbor_algo.run(adj_matrix)

    print(f"tour: {tour}")
    print(f"total_cost: {total_cost}")



