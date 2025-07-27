import struct

def finalize_hash(self, directory):
    with open(self.dir_file, "wb") as f:
        f.write(struct.pack("<i", directory.dir_depth))
        f.write(struct.pack("<i", len(directory.refs)))
        for ref in directory.refs:
            f.write(struct.pack("<i", ref))