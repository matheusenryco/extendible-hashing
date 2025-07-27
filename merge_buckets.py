from insert_operation import write_bucket_file
from buckets_dir import Bucket

def merge_buckets(self, ref_bk, bucket, ref_buddy, buddy_bucket):
    """
    Merges two buckets into one.
    Returns the merged bucket.
    """
    
    # Copy keys from buddy_bucket to bucket
    bucket.keys.extend(buddy_bucket.keys)
    
    # Update bucket.count and decrement bucket.depth
    bucket.count = len(bucket.keys)
    bucket.depth -= 1
    
    write_bucket_file(self, ref_bk, bucket)
    
    # Remove buddy_bucket from ref_buddy in the buckets file
    # (Creating an empty bucket to "remove" the buddy bucket)
    empty_bucket = Bucket(0)
    empty_bucket.count = 0
    empty_bucket.keys = []
    write_bucket_file(self, ref_buddy, empty_bucket)
    
    return bucket