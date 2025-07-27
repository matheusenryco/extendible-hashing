from insert_key_bucket import insert_key_bucket
from buckets_dir import MAX_BUCKET_SIZE
from search_operation import search_operation
import struct

def insert_operation(self, key):
    """
    Manages the insertion of a key in the extendible hashing.
    Returns False if the key already exists, True if it was successfully inserted.
    """
    
    found, ref_bk, found_bucket = search_operation(self, key)
    
    # If the key is found, insert_operation returns False and terminates
    if found:
        return False  # duplicate key
    
    # Otherwise, insert_operation calls insert_key_bucket passing the bucket where insertion will be made
    insert_key_bucket(self, key, ref_bk, found_bucket)
    return True

def write_bucket_file(self, ref_bk, bucket):
    with open(self.bucket_file, "r+b") as f:      
        f.write(struct.pack("<i", bucket.depth))
        f.write(struct.pack("<i", bucket.count))
        
        for i in range(MAX_BUCKET_SIZE):
            if i < len(bucket.keys):
                f.write(struct.pack("<i", bucket.keys[i]))
            else:
                f.write(struct.pack("<i", 0))  # 0 = empty slot