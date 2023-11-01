from CSVParser_Packages import CSVParser_Packages  # authored by student
from HashTable import HashTable  # authored by student

class TestPackageManager:

    def __init__(self, package_manager):
        self.test_parsing_40()
        self.test_duplicate_ids(package_manager)

    def test_parsing_40(self):
        packages_parser = CSVParser_Packages("packages.csv")
        package_tuples = packages_parser.parse2()  # tuple is: (package_id, package_object)
        my_hash_table = HashTable(len(package_tuples))
        for package_tuple in package_tuples:
            my_hash_table.add(package_tuple[0], package_tuple[1])

        if my_hash_table.how_many_packages() != 40:
            print(f"Test Failure: there should be 40 packages.")
        else:
            print(f"Test Success: 40 packages read from packages.csv")

    def test_duplicate_ids(self, package_manager):
        packages = package_manager.get_all_packages()
        package_ids = {package.id_unique for package in packages}
        num_packages = len(packages)
        num_ids = len(package_ids)
        print(f"num_packages: {num_packages} num_ids: {num_ids}")
        if num_packages != num_ids:
            print(f"Test Failure: there should be no duplicate package ids")
        else:
            print(f"Test Success: there are no duplicate package ids")