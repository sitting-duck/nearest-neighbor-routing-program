from enum import Enum, auto

class Status(Enum):
    """
    An enumeration representing the status of a package.

    Attributes:
    - hub (int): The package is at the hub.
    - enroute (int): The package is en route to its destination.
    - delivered (int): The package has been delivered.
    """
    hub = 0
    enroute = 1
    delivered = 2

class Package:
    """
    A class representing a package in a delivery system.

    Attributes:
    - id_unique (str): A unique identifier for the package.
    - address (str): The delivery address of the package.
    - deadline (str): The delivery deadline for the package.
    - city (str): The city of the delivery address.
    - state (str): The state of the delivery address.
    - zip_code (str): The ZIP code of the delivery address.
    - weight (float): The weight of the package.
    - status (Status): The current status of the package.
    - delivery_time (int): The delivery time of the package.
    - note (str): Additional notes or information about the package.
    """
    def __init__(self, id_unique, address, deadline, city, state, zip_code, weight, status, delivery_time, note):
        """
        Initialize a Package object with the given attributes.

        Parameters:
        - id_unique (str): Unique identifier for the package.
        - address (str): Delivery address.
        - deadline (str): Delivery deadline.
        - city (str): City of the delivery address.
        - state (str): State of the delivery address.
        - zip_code (str): ZIP code of the delivery address.
        - weight (float): Weight of the package.
        - status (Status): Current status of the package.
        - delivery_time (int): Delivery time of the package.
        - note (str): Additional notes about the package.
        """
        self.id_unique = id_unique
        self.address = address
        self.deadline = deadline
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.weight = weight
        self.status = status
        self.delivery_time = delivery_time
        self.note = note

    def __str__(self):
        """
        Returns a string representation of the Package object.

        Returns:
        - str: A string representing the package with its attributes.
        """
        return (f'id: {self.id_unique} \naddress: {self.address}\n deadline: {self.deadline}\n city: {self.city}\n zip: {self.zip_code}\n '
                f'weight: {self.weight}\n status: {self.status}\n delivery_time: {self.delivery_time}\n note: {self.note}\n')

    def __repr__(self):
        """
        Returns a string representation of the Package object.
        Ideal for debugging and logging.

        Returns:
        - str: A string representing the package.
        """
        return self.__str__()

    def same_address(self, address, city, zip_code):
        """
        Check if the package has the same address as the given address, city, and zip code.

        Parameters:
        - address (str): Address to compare.
        - city (str): City to compare.
        - zip_code (str): ZIP code to compare.

        Returns:
        - bool: True if the address, city, and ZIP code match; False otherwise.
        """
        return self.address == address and self.city == city and self.zip_code == zip_code

    def get_address_string(self):
        """
        Get a formatted address string for the package.

        Returns:
        - str: The formatted address string.
        """
        return self.address + ", " + self.city + ", " + self.state + " " + self.zip_code

    def set_delivery_time(self, delivery_time):
        """
        Set a delivery time string for the package.

        Returns:
        - nothing
        """
        self.delivery_time = delivery_time

    def set_status(self, status):
        """
        Set a status string for the package.

        Returns:
        - nothing
        """
        self.status = status
