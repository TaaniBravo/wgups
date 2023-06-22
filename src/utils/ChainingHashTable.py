# HashTable class using chaining.
from typing import Any


class ChainingHashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity: int = 10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def get_bucket_list(self, key: Any) -> list:
        """
        Returns the bucket list where the given key should be stored.
        :param key:
        :return:
        """
        bucket = hash(key) % len(self.table)
        return self.table[bucket]

    def insert(self, item: Any, key: Any) -> None:
        """
        Inserts a new item into the hashtable.
        Inserting based off a key and not the actual item allows to
        more accurately get objects with the same key value into the same bucket.
        Time Complexity: O(1)
        """
        # get the bucket list where this item will go.
        bucket_list = self.get_bucket_list(key)
        # insert the item to the end of the bucket list.
        bucket_list.append(item)

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, item: Any, key: Any) -> Any:
        # get the bucket list where this key would be.
        bucket_list = self.get_bucket_list(key)

        # search for the key in the bucket list
        if item in bucket_list:
            # find the item's index and return the item that is in the bucket list.
            item_index = bucket_list.index(item)
            return bucket_list[item_index]
        else:
            # the key is not found.
            return None

    # Removes an item with matching key from the hash table.
    def remove(self, key: Any) -> None:
        # get the bucket list where this item will be removed from.
        bucket_list = self.get_bucket_list(key)

        # remove the item from the bucket list if it is present.
        if key in bucket_list:
            bucket_list.remove(key)

    # Overloaded string conversion method to create a string
    # representation of the entire hash table. Each bucket is shown
    # as a pointer to a list object.
    def __str__(self):
        index = 0
        s = "   --------\n"
        for bucket in self.table:
            s += "%2d:|   ---|-->%s\n" % (index, bucket)
            index += 1
        s += "   --------"
        return s
