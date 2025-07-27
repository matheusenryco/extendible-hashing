from buckets_dir import MAX_BUCKET_SIZE
from find_buddy_bucket import find_buddy_bucket  
from merge_buckets import merge_buckets
from read_bucket_file import read_bucket_file
from try_decrease_dir import try_decrease_dir

def try_merge_buckets(self, ref_bk, bucket):
    """
    Tries to merge buckets after a removal to optimize space.
    """
    # Check if bucket has a buddy
    has_buddy, buddy_address = find_buddy_bucket(self, bucket)
    
    # If no buddy, then return (end)
    if not has_buddy:
        return
    
    buddy_bucket = read_bucket_file(self, buddy_address)
    
    # Check if bucket and buddy_bucket can be concatenated
    if (buddy_bucket.count + bucket.count) <= MAX_BUCKET_SIZE:
        buddy_ref = self.directory.refs[buddy_address]
        bucket = merge_buckets(self, ref_bk, bucket, buddy_ref, buddy_bucket)
        
        for i in range(len(self.directory.refs)):
            if self.directory.refs[i] == buddy_ref:
                self.directory.refs[i] = ref_bk
        
        # After concatenation, check if the directory can shrink in size
        if try_decrease_dir(self):
            # If the directory decrease, a new buddy may have appeared
            try_merge_buckets(self, ref_bk, bucket)  # recursion
