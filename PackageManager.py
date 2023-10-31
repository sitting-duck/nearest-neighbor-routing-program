
class PackageManager:

    def __init__(self, packages_hash_table):
        """
        Initialize an instance of the class.

        Parameters:
        - packages_hash_table (object): A hash table instance containing packages.

        Attributes:
        - packages_hash_table (object): The provided hash table is stored for further operations.
        """
        self.packages_hash_table = packages_hash_table

    def get_unique_locations(self, package_load, location_strings):
        unique_locations = []
        for package in package_load:
            unique_locations.append(package.get_address_string())
        unique_locations = list(set(unique_locations))
        return unique_locations

    def how_many_packages(self):
        """
        Retrieve the total number of packages in the manager's hash table.

        Returns:
        - int: The number of packages contained within the hash table.
        """
        return self.packages_hash_table.how_many_packages()

    def get_packages(self, howmany):
        """
        Fetch a specified number of packages from the manager's hash table.

        Parameters:
        - howmany (int): The number of packages to fetch from the hash table.

        Returns:
        - list: A list containing the specified number of package objects.
        """
        return self.packages_hash_table.get_n_packages(howmany)

    def does_package_exist(self, package_id):
        """
        Check if a package with the given package ID exists in the manager's hash table.

        Parameters:
        - package_id (int or str): The ID of the package to be checked.

        Returns:
        - bool: True if the package exists, False otherwise.
        """

        return True if self.packages_hash_table.get(package_id) else False

    def input_valid_package_id(self):
        """
        Prompt the user to enter a valid package id and keep asking until a valid package id is provided.
        Return the string representing the package id. The string "quit" is also an acceptable answer, as it allows the
        user to exit the command line interface for the program.
        """
        while True:
            package_id = input("Enter the package id in the format (e.g., '1', '2', '3') or 'quit' to exit: ")

            if package_id.lower() == "quit":
                return package_id

            if self.does_package_exist(package_id):
                return package_id
            else:
                print("Invalid package id. Package does not exist.")
