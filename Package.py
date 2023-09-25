from enum import Enum, auto
class Status(Enum):
    hub = 0
    enroute = 1
    delivered = 2

class Package:
    def __init__(self, address, deadline, city, zip_code, weight, status, delivery_time, note):
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.status = status
        self.delivery_time = delivery_time
        self.note = note

    def __str__(self):
        """
            Returns a string representation of the Location object.
            :return: A string representing the Package object.
        """
        return f"address: {self.address}\n deadline: {self.deadline}\n city: {self.city}\n zip: {self.zip_code}\n weight: {self.weight}\n status: {self.status}\n delivery_time: {self.delivery_time}\n note: {self.note}\n"

    def __repr__(self):
        """
            Returns a string representation of the Location object.
            :return: A string representing the Package object.
        """
        return self.__str__()
