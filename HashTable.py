import copy

class HashTable:
    """
    A simple hash table implementation for storing and managing packages.
    """

    def __init__(self, size=1000):
        """
        Initialize a hash table of the specified size.

        Parameters:
        - size (int, optional): The size of the hash table. Defaults to 1000.
        """
        if size < 0:
            raise ValueError("Size cannot be less than zero.")

        self.size = size
        self.table = [[] for _ in range(self.size)]
        self.num_buckets = 0

    def hash_function(self, key):
        """
        Compute a hash value for the provided key.

        Parameters:
        - key: The key to be hashed.

        Returns:
        - int: The hash index for the key.
        """
        try:
            int_key = int(key)
        except ValueError:
            raise ValueError(f"The key '{key}' cannot be converted to an integer.")

        return int_key % self.size

    def get_key_from_hash(self, key):
        """
        Retrieve package ID using the hash key.

        Parameters:
        - key: The key for which the package ID is to be retrieved.

        Returns:
        - int: The package ID.
        """
        return self.size - key

    def add(self, key, value):
        """
        Add a key-value pair to the hash table.

        Parameters:
        - key: The key for the entry.
        - value: The value associated with the key.
        """
        hash_index = self.hash_function(key)
        key_exists = False
        bucket = self.table[hash_index]

        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                key_exists = True
                break

        if key_exists:
            bucket[i] = ((key, value))
        else:
            bucket.append((key, value))

        self.num_buckets += 1

    def get(self, key):
        """
        LOOK UP FUNCTION
        Retrieve the value associated with a given key. ie. The "look up function"

        Parameters:
        - key (str): The key whose associated value is to be retrieved.

        Returns:
        - The value associated with the key or None if the key doesn't exist.
        """
        hash_index = self.hash_function(key)
        bucket = self.table[hash_index]

        for kv in bucket:
            k, v = kv
            if key == k:
                return v
        return None

    def get_copy(self, key):
        """
        Retrieve a copy of the value associated with a given key. Similar to the lookup function but non destructive.

        Parameters:
        - key (str): The key whose associated value is to be retrieved.

        Returns:
        - A deep copy of the value associated with the key or None if the key doesn't exist.
        """
        hash_index = self.hash_function(key)
        bucket = self.table[hash_index]

        for kv in bucket:
            k, v = kv
            if key == k:
                return copy.deepcopy(v)
        return None

    def delete(self, key):
        """
        Remove a key-value pair from the hash table using the specified key.

        Parameters:
        - key: The key of the entry to be removed.
        """
        hash_index = self.hash_function(key)
        bucket = self.table[hash_index]

        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                del bucket[i]

    def print(self):
        """Print all key-value pairs stored in the hash table."""
        for i, bucket in enumerate(self.table):
            if bucket:
                print(f"Bucket {i}:")
                for kv in bucket:
                    k, v = kv
                    print(f"  Key: {k}, Value: {v}")

# todo: get n buckets
    def get_n_buckets(self, num):
        """
        Fetch a specified number of package entries from the hash table. Note: the fetched packages will be
        removed from the array internally.

        Parameters:
        - num (int): The number of packages to fetch.

        Returns:
        - list: A list containing the specified number of package entries.
        """
        if len(self.table) >= num:
            howmany = num
        else:
            howmany = len(self.table)

        buckets = self.table[0:howmany]
        self.table = self.table[howmany:]
        self.num_buckets -= howmany

        package_list = []
        for bucket in buckets:
            package_list.append(bucket[0][1])
        return package_list

    def how_many_buckets(self):
        """
        Retrieve the total number of packages stored in the hash table.

        Returns:
        - int: The total number of packages.
        """
        return self.num_buckets

    def check_key_exists(self, id):
        """
        Check if a package with the given unique ID exists in the hash table.

        Parameters:
        - id: The unique identifier of the package to check.

        Returns:
        - bool: True if the package exists, False otherwise.
        """
        for package in self.table:
            if package.id_unique == id:
                return True
        return False


    def get_copy_all_buckets(self):
        """
        Get a copy of all package entries in the hash table.

        Returns:
        - list: A list of all package entries, each represented as a tuple of (key, value).
        """
        howmany = len(self.table)
        packages = self.table[0:howmany]
        package_list = []
        for package in packages:
            package_list.append(package[0][1])
        return package_list
