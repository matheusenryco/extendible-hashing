import struct
from dataclasses import dataclass
from buckets_dir import Bucket, Directory
import os

MAX_BUCKET_SIZE = 2  # Maximum bucket size

class ExtendibleHashing:
    def __init__(self, bucket_file, dir_file):
        self.bucket_file = bucket_file
        self.dir_file = dir_file

    def initialize_extendible_hashing(self):
        # if hashing exists:
        if os.path.exists(self.dir_file) and os.path.exists(self.bucket_file):
            with open(self.dir_file, "rb") as f_dir, open(self.bucket_file, "rb") as f_bk:
                dir_depth = struct.unpack("<i", f_dir.read(4))[0]

                size = 2 ** dir_depth
                
                # Reads records from directory file to a directory object
                refs = []
                num_refs = struct.unpack("<i", f_dir.read(4))[0]  # reads number of references
                for _ in range(num_refs):  # reads each reference (RRN)
                    refs.append(struct.unpack("<i", f_dir.read(4))[0])
                
                # Transfers read data to a directory object
                directory = Directory()
                directory.dir_depth = dir_depth
                directory.refs = refs
            return directory
        
        else: # if hashing doesn't exist
            directory = Directory()
            directory.dir_depth = 0
        
            empty_bucket = Bucket(0)
            
            # creates the bucket file
            with open(self.bucket_file, "wb") as f_bk:
                f_bk.write(struct.pack("<i", empty_bucket.depth))
                f_bk.write(struct.pack("<i", empty_bucket.count))
                for _ in range(MAX_BUCKET_SIZE):
                    f_bk.write(struct.pack("<i", 0))  # 0 represents empty slot
            
            # assigns bucket RRN (0) to directory
            directory.refs = [0]  # First bucket has RRN = 0
            return directory