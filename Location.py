import pprint
class Location:
    """A class representing a Location with a name, address, and distances to other locations.

    Example Usage:

    # Creating a Location object
    loc = Location(name="Library", address="123 Read St")

    # Adding distances to other locations
    loc.add_distance("Cafe", 0.5)
    loc.add_distance("Park", 1.2)

    # Printing the Location object
    print(loc)  # Output: Location(name=Library, address=123 Read St, distances={'Cafe': 0.5, 'Park': 1.2})

    """

    def __init__(self, name, address: str, distances: dict[str, float] = None):
        """
        Initializes a new Location object.

        :param name: The name of the location.
        :param address: The address of the location.
        :param distances: A dictionary representing the distances to other locations.
                          Keys are location names, and values are distances in float.
        """
        self.name = name                                             # the name of the location
        self.address = address                                       # The address of the location
        self.distances = distances if distances is not None else {}  # Distances to other locations

    def add_distance(self, address: str, distance: float):
        """
        Adds a distance to another location.

        :param address: The name of the other location.
        :param distance: The distance to the other location.
        """
        self.distances[address] = distance  # Add or update the distance to the specified location

    def __str__(self):
        """
        Returns a string representation of the Location object.

        :return: A string representing the Location object.
        """
        pretty_distances = pprint.pformat(self.distances, indent=4)
        return f"Location(address={self.address}, distances={pretty_distances})"

    def __repr__(self):
        """
        Returns the official string representation of the Location object.

        :return: A string representing the Location object.
        """
        return self.__str__()
