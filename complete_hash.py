from dataclasses import dataclass
import struct
import os
import sys

MAX_BUCKET_SIZE = 2 # Global variable to test changing the maximum size of bucket

def generate_address(key, depth):
    ''' 
    Takes any key, calculates its hash and generates an address
    Function that maps the return of the hash function to an
    address suitable for the directory
    ''' 
    # Reverses the address bits and extracts *depth* bits

    ret_val = 0  # Will store the bit sequence
    mask = 1     # Mask 0...001 to extract the least significant bit
    hash_val = hash(key)

    for _ in range(1, depth + 1):
        ret_val <<= 1
        # Extract the lowest order bit from hash_val

        low_order_bit = hash_val & mask
        # Insert low_order_bit at the end of ret_val
        ret_val |= low_order_bit
        hash_val >>= 1
    return ret_val

class Bucket:
    def __init__(self, depth):
        self.depth: int = depth  # stores the bucket depth
        self.count = 0
        self.keys = []  # list that stores up to MAX_BUCKET_SIZE keys

class Directory:
    def __init__(self):
        self.refs: list = []      # list of references (RRN) to buckets
        self.dir_depth: int = 0

class ExtendibleHashing:
    def __init__(self, bucket_file, dir_file):
        self.bucket_file = bucket_file
        self.dir_file = dir_file

## pseudocode slide 07 ##
    def initialize_extendible_hashing(self):
        # if hashing exists:
        if os.path.exists(self.dir_file) and os.path.exists(self.bucket_file):  # checks if files exist
            # Opens directory and bucket files
            with open(self.dir_file, "rb") as f_dir, open(self.bucket_file, "rb") as f_bk:
                dir_depth = struct.unpack("<i", f_dir.read(4))[0]

                size = 2 ** dir_depth
                
                # Reads records from directory file to a directory object
                refs = []
                num_refs = struct.unpack("<i", f_dir.read(4))[0]  # reads number of references
                for _ in range(num_refs):  # reads each reference (RRN)
                    refs.append(struct.unpack("<i", f_dir.read(4))[0])
                
                # Transfers read data to a directory object
                directory = Directory()
                directory.dir_depth = dir_depth
                directory.refs = refs
            return directory
        
        else:  # if hashing doesn't exist
            directory = Directory()
            directory.dir_depth = 0
            
            # creates an empty bucket in the bucket file
            empty_bucket = Bucket(0)
            
            # creates the bucket file
            with open(self.bucket_file, "wb") as f_bk:
                f_bk.write(struct.pack("<i", empty_bucket.depth))
                f_bk.write(struct.pack("<i", empty_bucket.count))
                for _ in range(MAX_BUCKET_SIZE):
                    f_bk.write(struct.pack("<i", 0))  # 0 represents empty slot
            
            # assigns bucket RRN (0) to directory
            directory.refs = [0]  # First bucket has RRN = 0
            return directory

def finalize_hash(self, directory):
    # Opens directory file and writes directory object
    with open(self.dir_file, "wb") as f:
        # Write directory object to directory file
        f.write(struct.pack("<i", directory.dir_depth))  # Writes dir_depth
        f.write(struct.pack("<i", len(directory.refs)))  # Writes number of references
        for ref in directory.refs:  # Writes each reference (RRN)
            f.write(struct.pack("<i", ref))

def search_operation(self, key):
    address = generate_address(key, self.directory.dir_depth)
    ref_bk = self.directory.refs[address]
    
    # Uses read_bucket_file function to get the bucket
    found_bucket = read_bucket_file(self, ref_bk)
    
    if key in found_bucket.keys:
        return True, ref_bk, found_bucket
    return False, ref_bk, found_bucket

def insert_key_bucket(self, key, ref_bk, bucket):
    """
    Tries to insert a key in the bucket. If there's space, inserts and finishes.
    If the bucket is full, calls split_bucket to perform the split.
    """
    
    # If insert_key_bucket finds space in the bucket for insertion
    if bucket.count < MAX_BUCKET_SIZE:
        # The key is inserted and the operation ends
        bucket.keys.append(key)
        bucket.count += 1
        write_bucket_file(self, ref_bk, bucket)
    else:
        # If the bucket is full, insert_key_bucket calls split_bucket to perform the split
        split_bucket(self, ref_bk, bucket)
        # When control returns, insert_operation is called for a new attempt
        # (indirect recursion - the cycle continues until finding an available bucket)
        insert_operation(self, key)

def split_bucket(self, ref_bk, bucket):
    """
    Performs bucket splitting when it's full.
    Determines if the directory needs to be expanded and redistributes keys.
    """
    
    # split_bucket first determines if the directory is large enough
    # to accommodate the new bucket
    if bucket.depth == self.directory.dir_depth:
        # If the directory needs to be expanded, split_bucket calls double_directory
        # to double the directory size
        double_directory(self)
    
    # split_bucket allocates a new bucket
    new_bucket = Bucket(bucket.depth)
    
    # Finds the next free RRN in the file
    with open(self.bucket_file, "r+b") as f:
        f.seek(0, 2)  # Goes to end of file
        file_size = f.tell()
        record_size = 8 + (MAX_BUCKET_SIZE * 4)
        ref_new_bucket = file_size // record_size
    
    # Links appropriate directory references
    new_start, new_end = find_new_interval(self, bucket)
    for i in range(new_start, new_end + 1):
        if i < len(self.directory.refs):
            self.directory.refs[i] = ref_new_bucket

    # Increments bucket depths
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
    
    # Writes both buckets to file
    write_bucket_file(self, ref_bk, bucket)
    write_bucket_file(self, ref_new_bucket, new_bucket)

def double_directory(self):
    """
    Doubles the directory size when necessary to accommodate new buckets.
    """
    
    new_refs = []
    # Insert each reference in directory.refs twice in new_refs
    for ref in self.directory.refs:
        new_refs.extend([ref] * 2)
        
    # Assign new_refs to directory.refs
    self.directory.refs = new_refs
    self.directory.dir_depth += 1

def write_bucket_file(self, ref_bk, bucket):
    with open(self.bucket_file, "r+b") as f:
        # Position at bucket RRN
        position = ref_bk * (8 + MAX_BUCKET_SIZE * 4)
        f.seek(position)
        
        f.write(struct.pack("<i", bucket.depth))
        f.write(struct.pack("<i", bucket.count))
        
        # Writes the keys
        for i in range(MAX_BUCKET_SIZE):
            if i < len(bucket.keys):
                f.write(struct.pack("<i", bucket.keys[i]))
            else:
                f.write(struct.pack("<i", 0))  # empty slot

def insert_operation(self, key):
    """
    Manages key insertion in extendible hashing.
    Returns False if key already exists, True if successfully inserted.
    """

    found, ref_bk, found_bucket = search_operation(self, key)
    
    # If key is found, insert_operation returns False and ends
    if found:
        return False  # duplicate key
    
    # Otherwise, insert_operation calls insert_key_bucket passing the bucket where insertion will be made
    insert_key_bucket(self, key, ref_bk, found_bucket)
    return True

def find_new_interval(self, bucket):
    # pseudocode slide 13
    mask = 1
    key = bucket.keys[0]
    common_address = generate_address(key, bucket.depth)
    common_address = common_address << 1
    common_address = common_address | mask
    bits_to_fill = self.directory.dir_depth - (bucket.depth + 1)
    new_start, new_end = common_address, common_address
    for i in range(bits_to_fill):
        new_start = new_start << 1
        new_end = new_end << 1
        new_end = new_end | mask
    return new_start, new_end

def remove_operation(self, key):
    """
    Removes a key from extendible hashing.
    Returns False if key doesn't exist, True if successfully removed.
    """
    
    found, ref_bk, found_bucket = search_operation(self, key)
    
    if not found:
        return False
    
    return remove_key_bucket(self, key, ref_bk, found_bucket)

def remove_key_bucket(self, key, ref_bk, bucket):
    """
    Removes a specific key from the bucket.
    Returns True if removed, False otherwise.
    """
    
    removed = False
    
    if key in bucket.keys:
        # Remove key from bucket and decrement bucket.count
        bucket.keys.remove(key)
        bucket.count -= 1
        write_bucket_file(self, ref_bk, bucket)
        removed = True
    
    if removed:
        try_merge_buckets(self, ref_bk, bucket)
        return True
    else:
        return False

def try_merge_buckets(self, ref_bk, bucket):
    """
    Tries to merge buckets after a removal.
    """
    
    # Check if bucket has a buddy
    has_buddy, buddy_address = find_buddy_bucket(self, bucket)
    
    # If no buddy, then return (end)
    if not has_buddy:
        return
    
    # Read the bucket from buddy_address and store in buddy_bucket
    buddy_bucket = read_bucket_by_address(self, buddy_address)
    
    # Check if bucket and buddy_bucket can be concatenated
    if (buddy_bucket.count + bucket.count) <= MAX_BUCKET_SIZE:
        buddy_ref = self.directory.refs[buddy_address]
        bucket = merge_buckets(self, ref_bk, bucket, buddy_ref, buddy_bucket)
        
        # Make the directory entry that pointed to buddy_bucket point to bucket
        for i in range(len(self.directory.refs)):
            if self.directory.refs[i] == buddy_ref:
                self.directory.refs[i] = ref_bk
        
        # After concatenation, check if the directory can shrink in size
        if try_shrink_directory(self):
            # If the directory shrinks, a new buddy may have appeared
            try_merge_buckets(self, ref_bk, bucket)

def find_buddy_bucket(self, bucket):
    """
    Finds the buddy bucket for possible merging.
    Returns (has_buddy, buddy_address).
    """
    # If dir_depth equals 0, then return False, None
    if self.directory.dir_depth == 0:
        return False, None
    
    # If bucket.depth < dir_depth, then return False, None
    if bucket.depth < self.directory.dir_depth:
        return False, None
    
    # Find the common_address of the keys contained in bucket
    if len(bucket.keys) == 0:
        return False, None
    
    # Use the first key to find the common address
    common_address = generate_address(bucket.keys[0], bucket.depth)
    
    # Find the address of the buddy bucket (buddy_address)
    # buddy_address = common_address with least significant bit inverted
    # buddy_address = common_address XOR_bitwise 1 (address ^ 1)
    buddy_address = common_address ^ 1
    
    # Return True, buddy_address
    return True, buddy_address

def read_bucket_file(self, ref_bk):
    """
    Reads a bucket from file based on RRN.
    """
    with open(self.bucket_file, "rb") as f:
        # Position at bucket RRN
        position = ref_bk * (8 + MAX_BUCKET_SIZE * 4)
        f.seek(position)
        
        # Read depth and counter
        depth = struct.unpack("<i", f.read(4))[0]
        count = struct.unpack("<i", f.read(4))[0]
        
        # Create bucket and read keys
        bucket = Bucket(depth)
        bucket.count = count
        bucket.keys = []
        
        for i in range(MAX_BUCKET_SIZE):
            key = struct.unpack("<i", f.read(4))[0]
            if key != 0:  # Only 0 indicates empty slot
                bucket.keys.append(key)
        return bucket

def read_bucket_by_address(self, address):
    """
    Reads a bucket from file based on directory address.
    """
    ref_bk = self.directory.refs[address]
    return read_bucket_file(self, ref_bk)

def merge_buckets(self, ref_bk, bucket, buddy_ref, buddy_bucket):
    """
    Merges two buckets into one.
    Returns the merged bucket.
    """
    # Copy keys from buddy_bucket to bucket
    bucket.keys.extend(buddy_bucket.keys)
    
    # Update bucket.count and decrement bucket.depth
    bucket.count = len(bucket.keys)
    bucket.depth -= 1
    
    # Rewrite bucket at ref_bk in buckets file
    write_bucket_file(self, ref_bk, bucket)
    
    # Remove buddy_bucket from buddy_ref in buckets file
    # (Creating an empty bucket to "remove" the buddy bucket)
    empty_bucket = Bucket(0)
    empty_bucket.count = 0
    empty_bucket.keys = []
    write_bucket_file(self, buddy_ref, empty_bucket)
    
    # Return bucket
    return bucket

def try_shrink_directory(self):
    """
    Tries to shrink directory size if possible.
    Returns True if shrunk, False otherwise.
    """
    # If dir_depth equals 0, then return False
    if self.directory.dir_depth == 0:
        return False
    
    # Set dir_size to 2 ^ dir_depth
    dir_size = 2 ** self.directory.dir_depth
    
    # Set shrink to True (assume it's possible and try to prove otherwise)
    shrink = True
    
    # For i = 0 to dir_size - 1 with step 2
    for i in range(0, dir_size, 2):
        # If directory.refs[i] != directory.refs[i+1] then
        if self.directory.refs[i] != self.directory.refs[i + 1]:
            # Set shrink to False
            shrink = False
            # Break the loop
            break
    
    # If shrink then:
    if shrink:
        # Create a list new_refs
        new_refs = []
        
        # For each two references from current refs, insert one in new_refs
        for i in range(0, dir_size, 2):
            new_refs.append(self.directory.refs[i])
        
        # Set directory.refs to new_refs
        self.directory.refs = new_refs
        
        # Decrement dir_depth
        self.directory.dir_depth -= 1
    return shrink

def print_directory(self):
    """Prints the current directory state."""
    
    print("---- Directory ----")
    for i in range(len(self.directory.refs)):
        print(f"dir[{i}] = bucket[{self.directory.refs[i]}]")
    
    print()
    print(f"Depth = {self.directory.dir_depth}")
    print(f"Current size = {len(self.directory.refs)}")
    
    # Count unique referenced buckets
    unique_buckets = len(set(self.directory.refs))
    print(f"Total buckets = {unique_buckets}")

def print_buckets(self):
    """Prints bucket contents"""
    
    print("---- Buckets ----")
    
    bucket_size = struct.calcsize(f"<ii{MAX_BUCKET_SIZE}i")
    with open(self.bucket_file, "rb") as f:
        file_data = f.read()
    file_size = len(file_data)
    total_buckets = file_size // bucket_size
    
    # Identifies which buckets are being referenced
    referenced_buckets = []
    for ref in self.directory.refs:
        if ref not in referenced_buckets:
            referenced_buckets.append(ref)
    
    for rrn in range(total_buckets):
        bucket = read_bucket_file(self, rrn)
        
        # Checks if bucket was removed or is not being referenced
        if bucket.depth == -1 or rrn not in referenced_buckets:
            print(f"Bucket {rrn} -- Removed")
            print()  # Blank line after removed bucket
        else:
            print(f"Bucket {rrn} (Depth = {bucket.depth}):")
            print(f"Key_count: {bucket.count}")
            
            # Fill keys with 0 until completing MAX_BUCKET_SIZE
            keys_to_show = bucket.keys[:]
            for _ in range(MAX_BUCKET_SIZE - len(keys_to_show)):
                keys_to_show.append(0)
                
            print(f"Keys = {keys_to_show}")
            print()

if __name__ == "__main__":
    operation_file = None
    print_directory_flag = False
    print_buckets_flag = False
    
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg == "-e" or arg == "--exec":
            if i + 1 < len(sys.argv):
                operation_file = sys.argv[i + 1]
        elif arg == "-pd" or arg == "--print-directory":
            print_directory_flag = True
        elif arg == "-pb" or arg == "--print-buckets":
            print_buckets_flag = True

    # Create extendible hashing instance
    hashing = ExtendibleHashing("buckets.dat", "directory.dat")
    hashing.directory = hashing.initialize_extendible_hashing()

    if print_directory_flag and not operation_file:
        print_directory(hashing)

    elif print_buckets_flag and not operation_file:
        print_buckets(hashing)
  
    if operation_file:
        try:
            with open(operation_file, "r") as f:
                for line in f:
                    # Remove line breaks and extra spaces
                    line = line.strip()
                    if len(line) > 0:
                        # Separate operation and key
                        parts = line.split()
                        if len(parts) >= 2:
                            op = parts[0]
                            key_str = parts[1]
                            key = int(key_str)

                            if op.lower() == 'i':
                                if insert_operation(hashing, key):
                                    print(f"> Key {key} insertion: Success.")
                                else:
                                    print(f"> Key {key} insertion: Failed - Duplicate key.")
                            elif op.lower() == 'b':
                                found, ref_bk, bucket = search_operation(hashing, key)
                                if found:
                                    print(f"> Search for key {key}: Key found in bucket {ref_bk}.")
                                else:
                                    print(f"> Search for key {key}: Key not found.")
                            elif op.lower() == 'r':
                                if remove_operation(hashing, key):
                                    print(f"> Key {key} removal: Success.")
                                else:
                                    print(f"> Key {key} removal: Failed - Key not found.")
                            else:
                                print(f"Unknown operation: {op}")
            
            # Finalize by saving state
            finalize_hash(hashing, hashing.directory)
            
            if print_directory_flag:
                print()  # Blank line to separate
                print_directory(hashing)
            
            if print_buckets_flag:
                print()  # Blank line to separate
                print_buckets(hashing)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
