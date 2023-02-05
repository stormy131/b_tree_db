# THIS FILE CONTAINS IMPLEMENTATION OF DATABASE AGENT

import os
import pickle
from b_tree import BTree

class DB_Agent:
    # degree - DEGREE OF A B-TREE IN DATABASE
    # file_caching - SET TO FALSE, IF DON`T WANT TO SAVE DATA TO FILE
    def __init__(self, degree, file_caching=True):
        self.tree = BTree(degree)
        self.key_template = None

        if file_caching:
            self.file_path = 'storage.txt'

            # IF DATA FILE ALREADY EXISTS - TRY TO READ EXISTING DATA AND PUT IT IN TREE
            if os.path.exists(self.file_path):
                with open(self.file_path, mode='rb') as f:
                    self.tree = pickle.load(f)

    # LOAD DATABASE DATA FROM SOME FILE
    # file_from - FILE WITH DATABASE DATA
    def provide_data(self, file_from):
        assert os.path.exists(file_from)
        with open(file_from, mode='rb') as f:
            self.tree = pickle.load(f)

    # 'PRIVATE' METHOD (NOT FOR USAGE).
    # CHECKS THE TYPING OF THE PASSED KEY
    # key - KEY TO CHECK TYPING
    def check_key_type(self, key):
        if self.key_template is None:
            self.key_template = key

        assert type(self.key_template) == type(key)

    # FIND VALUE IN DATABASE USING PROVIDED KEY
    # key - KEY TO SEARCH FOR IN THE DATABASE
    def find(self, key):
        self.check_key_type(key)
        res = self.tree.search(key)
        return res[1] if res is not None else None

    # CREATE A RECORD IN THE DATABASE
    # key, value - KEY-VALUE PAIR TO BE IN THE NEW RECORD
    def insert_pair(self, key, value):
        self.check_key_type(key)
        self.tree.insert((key, value))

    # DELETE RECORD FROM THE DATABASE USING PROVIDED KEY
    # key - KEY TO SEARCH FOR IN THE DATABASE
    def delete_by_key(self, key):
        self.check_key_type(key)
        self.tree.remove_key(key)

    # SAVE DATABASE RECORDS TO 'storage.txt', IF THE 'file_caching' WAS ENABLED
    def save_data(self):
        if hasattr(self, 'file_path'):
            with open(self.file_path, mode='wb') as f:
                pickle.dump(self.tree, f)

    # PRINT DATABASE-TREE STRUCTURE LEVEL-BY-LEVEL
    def print_tree(self):
        self.tree.print_tree(self.tree.root)
