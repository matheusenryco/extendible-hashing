from search_operation import search_operation
from remove_key_bucket import remove_key_bucket

def remove_operation(self, key):
    """
    Remove a key from the extendible hashing.
    Returns False if the key doesn't exist, True if it was successfully removed.
    """
    
    found, ref_bk, found_bucket = search_operation(self, key)
    
    if not found:
        return False
    return remove_key_bucket(self, key, ref_bk, found_bucket)