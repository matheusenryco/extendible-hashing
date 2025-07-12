## pseudocode slide 05 ##

from dataclasses import dataclass

MAX_BUCKET_SIZE = 2  # setting the maximum bucket size as 2

class Bucket:
    def __init__(self, depth):
        self.depth: int = depth # stores the bucket depth
        self.count = 0 # int that stores the number of keys in the bucket
        self.keys = []

class Directory:
    def __init__(self):
        self.refs: list = [] # list of references (RRN) to buckets
        self.dir_depth: int = 0 # int that stores the directory depth