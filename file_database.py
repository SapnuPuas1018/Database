import pickle
import os
import logging
from dict_database import DictDatabase

FILE_PATH = 'database.pkl'

class FileDatabase(DictDatabase):
    def __init__(self):
        """
        Initializes an instance of the FileDatabase class, extending DictDatabase.
        Loads an existing dictionary from a file or initializes a new one if the file does not exist.
        """
        super().__init__()
        logging.info("Initializing FileDatabase.")
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'wb') as database_file:
                pickle.dump(self.dict, database_file)  # Initialize with an empty dictionary
            logging.info("FileDatabase initialized with an empty dictionary.")
        else:
            with open(FILE_PATH, 'x') as database_file:
                pickle.dump(self.dict, database_file)
            logging.info("FileDatabase created a new database file with an empty dictionary.")

    def save(self):
        """
                Saves the current dictionary state to a file.

                :return: None
                :rtype: None
        """
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'wb') as database_file:
                pickle.dump(self.dict, database_file)
            logging.info("Database saved to file.")

    def load(self):
        """
                Loads the dictionary state from a file, if it exists. If the file does not exist,
                initializes with an empty dictionary.

                :return: None
                :rtype: None
        """
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'rb') as database_file:
                self.dict = pickle.load(database_file)
            logging.info("Database loaded from file.")
        else:
            self.dict = {}
            logging.warning("Database file not found. Initialized with an empty dictionary.")

    def set_value(self, val, key):
        """
                Sets a value in the dictionary for a specified key, then saves the updated dictionary to the file.

                :param val: The value to store in the dictionary.
                :type val: any
                :param key: The key to associate with the value.
                :type key: str
                :return: True if the operation is successful, False otherwise.
                :rtype: bool
        """
        self.load()
        response = super().set_value(val, key)
        self.save()
        return response

    def get_value(self, key):
        """
                Retrieves the value associated with the specified key in the dictionary, after loading the dictionary from the file.

                :param key: The key for which to retrieve the value.
                :type key: str
                :return: The value associated with the key if it exists, otherwise None.
                :rtype: any or None
        """
        self.load()
        val = super().get_value(key)
        logging.info(f"Returning value: {val} for key: {key}")
        return val

    def delete_value(self, key):
        """
                Deletes the key-value pair associated with the specified key from the dictionary, then saves the updated dictionary to the file.

                :param key: The key of the key-value pair to delete.
                :type key: str
                :return: The value associated with the deleted key if it exists, otherwise None.
                :rtype: any or None
        """
        self.load()
        val = super().delete_value(key)
        self.save()
        return val


if __name__ == '__main__':
    # Set up logging
    logging.basicConfig(filename='file_database.log', level=logging.DEBUG)

    # Test cases with assertions
    db = FileDatabase()

    # Test set_value
    assert db.set_value(10, 'a') == True, "Failed to set key 'a'"
    assert db.get_value('a') == 10, "Failed to get value for key 'a'"

    # Test update value
    assert db.set_value(20, 'a') == True, "Failed to update key 'a'"
    assert db.get_value('a') == 20, "Failed to get updated value for key 'a'"

    # Test get_value for non-existent key
    assert db.get_value('b') is None, "Non-existent key 'b' should return None"

    # Test delete_value
    assert db.delete_value('a') == 20, "Failed to delete key 'a'"
    assert db.get_value('a') is None, "Key 'a' should be deleted and return None"

    # Test delete_value for non-existent key
    assert db.delete_value('b') is None, "Deleting non-existent key 'b' should return None"

    logging.info("All assertions passed.")
    print("All assertions passed.")