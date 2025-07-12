## pseudocode slide 04 ##

''' 
takes any key, calculates its hash and generates an address
function that maps the return of the hash function to an
address suitable for the directory
'''

def generate_address(key, depth): 
    # Reverse the bits of the address and extract *depth* bits

    return_val = 0 # Will store the bit sequence
    mask = 1 # Mask 0...001 to extract the least significant bit
    hash_val = hash(key)

    for j in range(1, depth + 1):
        return_val <<= 1
        # Extract the lowest order bit from hash_val

        low_order_bit = hash_val & mask
        # Insert low_order_bit at the end of return_val
        return_val |= low_order_bit
        hash_val >>= 1
    return return_val