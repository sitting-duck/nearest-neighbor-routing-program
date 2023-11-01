from CSVParser_Packages import CSVParser_Packages  # authored by student
from HashTable import HashTable  # authored by student

class PackageManager:

    def __init__(self):
        """
        """
        packages_parser = CSVParser_Packages("packages.csv")
        package_tuples = packages_parser.parse2()  # tuple is: (package_id, package_object)
        my_hash_table = HashTable(len(package_tuples))
        for package_tuple in package_tuples:
            my_hash_table.add(package_tuple[0], package_tuple[1])
        self.packages_hash_table = my_hash_table

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

    def get_all_packages(self):
        """
        Fetch all packages from the manager's hash table. Note, this will empty the array of packages internally.

        Returns:
        - list: A list containing the package objects.
        """
        howmany = self.packages_hash_table.how_many_packages()
        return self.packages_hash_table.get_n_packages(howmany)
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
        # try:
        #     if self.packages_hash_table.get(package_id):
        #         print(f"package with id: {package_id} does exist")
        #         return True
        #     else:
        #         print(f"package with id {package_id} does NOT exist")
        #         return False
        # except:
        #     print(f"package with id {package_id} does NOT exist")
        #     return False
        #
        # return True if self.packages_hash_table.get(package_id) else False
        if self.packages_hash_table.check_id_exists(package_id):
            print(f"package with id: {package_id} exists.")
            return True
        else:
            print(f"package with id: {package_id} does NOT exist.")

    def print_all_package_ids(self):
        packages = self.packages_hash_table.get_copy_all_packages()
        for package in packages:
            print(package.id_unique, end=" ")

    def get_all_package_ids(self):
        ids = []
        packages = self.packages_hash_table.get_copy_all_packages()
        for package in packages:
            ids.append(package.id_unique)
        return ids

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
