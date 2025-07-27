import struct
from buckets_dir import MAX_BUCKET_SIZE, Bucket

def read_bucket_file(self, address):
    """
    Reads a bucket from the file based on the directory address.
    """
    ref_bk = self.directory.refs[address]
    
    with open(self.bucket_file, "rb") as f:
        # Position at the bucket's RRN
        position = ref_bk * (8 + MAX_BUCKET_SIZE * 4)
        f.seek(position)
        
        # Read depth and counter
        depth = struct.unpack("<i", f.read(4))[0]
        count = struct.unpack("<i", f.read(4))[0]
        
        # Create bucket and read the keys
        bucket = Bucket(depth)
        bucket.count = count
        bucket.keys = []
        
        for i in range(MAX_BUCKET_SIZE):
            key = struct.unpack("<i", f.read(4))[0]
            if key != -1:  # -1 indicates empty slot
                bucket.keys.append(key)
        
        return bucket
