class HashTable2:
    def __init__(self, size=1000):
        if size < 0:
            raise ValueError("Size cannot be less than zero.")

        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        self.check_type(key)
        return hash(key)

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

    def check_type(self, value):
        if not isinstance(value, (int, float, str)):
            raise ValueError("The variable must be of type int, float, or str")