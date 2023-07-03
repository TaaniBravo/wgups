from typing import Any


class HashTable:
    # Create empty bucket list of given size
    def __init__(self, size: int = 20):
        self.size = size
        self.hash_table = self.create_buckets()

    def create_buckets(self):
        return [[] for _ in range(self.size)]

    def __get_bucket__(self, key):
        hashed_key = hash(key) % self.size
        return self.hash_table[hashed_key]

    # Insert values into hash map
    def set_val(self, key, val):
        bucket = self.__get_bucket__(key)

        for index, record in enumerate(bucket):
            record_key, record_val = record
            # check if the bucket has same key as
            # the key to be inserted
            if record_key == key:
                bucket[index] = (key, val)
                return

        bucket.append((key, val))

    # Return searched value with specific key
    def get_val(self, key) -> Any:
        bucket = self.__get_bucket__(key)

        for index, record in enumerate(bucket):
            record_key, record_val = record

            # check if the bucket has same key as
            # the key being searched
            if record_key == key:
                return record_val

        return None

    # Remove a value with specific key
    def delete_val(self, key):
        bucket = self.__get_bucket__(key)

        for index, record in enumerate(bucket):
            record_key, record_val = record

            # check if the bucket has same key as
            # the key to be deleted
            if record_key == key:
                bucket.remove(record)
                return
