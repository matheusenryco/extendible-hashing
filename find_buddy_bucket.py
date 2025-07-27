def find_buddy_bucket(self, bucket):
    """
    Finds the buddy bucket for possible merging.
    Returns (has_buddy, buddy_address).
    """
    
    if self.directory.dir_depth == 0:
        return False, None
   
    if bucket.depth < self.directory.dir_depth:
        return False, None
    
    # Find the common_address of the keys contained in bucket
    if len(bucket.keys) == 0:
        return False, None
    
    # Use the first key to find the common address
    from generate_address import generate_address
    common_address = generate_address(bucket.keys[0], bucket.depth)
    
    # Find the address of the buddy bucket (buddy_address)
    # buddy_address = common_address with least significant bit inverted
    # buddy_address = common_address XOR_bitwise 1 (address ^ 1)
    buddy_address = common_address ^ 1
    
    return True, buddy_address
