from double_directory import double_directory
from buckets_dir import Bucket
from find_new_interval import find_new_interval
from insert_operation import write_bucket_file

def split_bucket(self, ref_bk, bucket):
    """
    Splits the bucket when it's full.
    Determines if the directory needs to be expanded and redistributes the keys.
    """
    
    # split_bucket first determines if the directory is large enough
    # to accommodate the new bucket
    if bucket.depth == self.directory.dir_depth:
        # If the directory needs to be expanded, split_bucket calls double_directory
        # to double the size of the directory
        double_directory(self)
    
    # split_bucket allocates a new bucket
    new_bucket = Bucket(bucket.depth)
    ref_new_bucket = len(self.directory.refs)  # next available RRN
    
    # Links the appropriate directory references
    new_start, new_end = find_new_interval(bucket)
    for i in range(new_start, new_end + 1):
        if i < len(self.directory.refs):
            self.directory.refs[i] = ref_new_bucket

    # Increments depth of both buckets
    bucket.depth += 1
    new_bucket.depth = bucket.depth
    
    # Redistributes keys between the two buckets
    old_keys = bucket.keys.copy()
    bucket.keys = []
    bucket.count = 0
    new_bucket.keys = []
    new_bucket.count = 0
    
    for key in old_keys:
        # Uses the new depth bit to redistribute
        if (hash(key) >> (bucket.depth - 1)) & 1:
            new_bucket.keys.append(key)
            new_bucket.count += 1
        else:
            bucket.keys.append(key)
            bucket.count += 1
    
    # Writes both buckets to the file
    write_bucket_file(self, ref_bk, bucket)
    write_bucket_file(self, ref_new_bucket, new_bucket)