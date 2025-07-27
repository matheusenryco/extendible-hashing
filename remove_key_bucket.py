from insert_operation import write_bucket_file
from try_merge import try_merge_buckets

def remove_key_bucket(self, key, ref_bk, bucket):
    """
    Remove a specific key from the bucket.
    Returns True if removed, False otherwise.
    """
    
    removed = False
    
    if key in bucket.keys:
        bucket.keys.remove(key)
        bucket.count -= 1
        
        write_bucket_file(self, ref_bk, bucket)
        
        removed = True
    
    if removed:
        try_merge_buckets(self, ref_bk, bucket)
        return True
    else:
        return False