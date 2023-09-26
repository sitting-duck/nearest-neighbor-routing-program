class HashTable:
    def __init__(self, size=1000):
        if size < 0:
            raise ValueError("Size cannot be less than zero.")

        self.size = size
        self.table = [[] for _ in range(self.size)]
        self.num_packages = 0

    def hash_function(self, key):
        try:
            int_key = int(key)
        except ValueError:
            raise ValueError(f"The key '{key}' cannot be converted to an integer.")

        return int_key % self.size

    def get_package_id_from_hash(self, key):
        return self.size - key
    def string_hash(input_string: str) -> int:
        # Define a prime number as a base for modulo operation to limit the hash value's size
        mod_base = 2 ** 32 - 1

        # Initialize hash value to 0
        hash_value = 0

        for char in input_string:
            # Update hash value by adding the ASCII value of the character
            hash_value = (hash_value + ord(char)) % mod_base

        return hash_value

    def add(self, key, value):
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

        self.num_packages += 1

    def get(self, key):
        hash_index = self.hash_function(key)
        bucket = self.table[hash_index]

        for kv in bucket:
            k, v = kv
            if key == k:
                return v
        return None

    def delete(self, key):
        hash_index = self.hash_function(key)
        bucket = self.table[hash_index]

        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                del bucket[i]

    def print(self):
        for i, bucket in enumerate(self.table):
            if bucket:
                print(f"Bucket {i}:")
                for kv in bucket:
                    k, v = kv
                    print(f"  Key: {k}, Value: {v}")

    def get_n_packages(self, num):
        packages = self.table[0:num] # grab num packages
        self.table = self.table[num:] # remove the packages from table
        self.num_packages -= num
        return packages

    def how_many_packages(self):
        return self.num_packages