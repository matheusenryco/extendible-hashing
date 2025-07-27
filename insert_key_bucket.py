from insert_operation import write_bucket_file
from split_bucket import split_bucket
from buckets_dir import MAX_BUCKET_SIZE
from insert_operation import insert_operation

def insert_key_bucket(self, key, ref_bk, bucket):
    """
    Tries to insert a key in the bucket. If there's space, inserts and finishes.
    If the bucket is full, calls split_bucket to perform the split.
    """
    
    # If insert_key_bucket finds space in the bucket for insertion
    if bucket.count < MAX_BUCKET_SIZE:
        # The key is inserted and the operation finishes
        bucket.keys.append(key)
        bucket.count += 1
        write_bucket_file(self, ref_bk, bucket)
    else:
        # If the bucket is full, insert_key_bucket calls split_bucket to perform the split
        split_bucket(self, ref_bk, bucket)
        # When control returns, insert_operation is called for a new attempt
        insert_operation(self, key)