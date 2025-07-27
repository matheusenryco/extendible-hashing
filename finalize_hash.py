import struct

def finalize_hash(self, directory):
    with open(self.dir_file, "wb") as f:
        # Write the directory object to the directory file
        f.write(struct.pack("<i", directory.dir_depth))  # Writes dir_depth
        f.write(struct.pack("<i", len(directory.refs)))  # Writes number of references
        for ref in directory.refs:  # Writes each reference (RRN)
            f.write(struct.pack("<i", ref))