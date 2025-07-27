from dataclasses import dataclass
from generate_address import generate_address
from buckets_dir import Bucket, Directory, MAX_BUCKET_SIZE
import struct

def search_operation(self, key):
    address = generate_address(key, self.dir_depth)
    ref_bk = self.directory.refs[address]
    
    # Read the bucket from ref_bk to found_bucket
    with open(self.bucket_file, "rb") as f:
        depth = struct.unpack("<i", f.read(4))[0]
        count = struct.unpack("<i", f.read(4))[0]
        keys = []
        for _ in range(MAX_BUCKET_SIZE):
            read_key = struct.unpack("<i", f.read(4))[0]
            if read_key != -1:
                keys.append(read_key)
    
    found_bucket = Bucket(depth)
    found_bucket.keys = keys
    found_bucket.count = count
    
    if key in found_bucket.keys:
        return True, ref_bk, found_bucket
    return False, ref_bk, found_bucket