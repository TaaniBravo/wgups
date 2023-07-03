from typing import Any


class HashTable:
    def __init__(self, size: int = 20):
        self.size = size
        self.hash_table = self.create_buckets()

    def create_buckets(self):
        """
        Creates empty buckets in the hash table
        Time complexity: O(n)
        Space complexity: O(n)
        :return:
        """
        return [[] for _ in range(self.size)]

    def __get_bucket__(self, key):
        """
        Returns the bucket that contains the key
        Time complexity: O(1)
        Space complexity: O(1)
        :param key:
        :return:
        """
        hashed_key = hash(key) % self.size
        return self.hash_table[hashed_key]

    # Insert values into hash map
    def set_val(self, key, val):
        """
        Inserts a value into the hash table
        Time complexity: O(n)
        Space complexity: O(n)
        :param key:
        :param val:
        :return:
        """
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
        """
        Returns a value from the hash table
        Time complexity: O(n)
        Space complexity: O(n)
        :param key:
        :return:
        """
        bucket = self.__get_bucket__(key)

        for index, record in enumerate(bucket):
            record_key, record_val = record

            # check if the bucket has same key as
            # the key being searched
            if record_key == key:
                return record_val

        return None

