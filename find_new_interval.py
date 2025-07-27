from generate_address import generate_address

def find_new_interval(self, bucket):
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