def try_decrease_dir(self):
    """
    Tries to decreases the directory size if possible.
    Returns True if it diminished, False otherwise.
    """
    
    if self.directory.dir_depth == 0:
        return False
    
    # Set dir_size to 2 ^ dir_depth
    dir_size = 2 ** self.directory.dir_depth
    decrease = True

    for i in range(0, dir_size, 2):
        if self.directory.refs[i] != self.directory.refs[i + 1]:
            decrease = False
            break
    
    if decrease:
        new_refs = []
        
        for i in range(0, dir_size, 2):
            new_refs.append(self.directory.refs[i])
        
        self.directory.refs = new_refs
        
        # Decrement dir_depth
        self.directory.dir_depth -= 1
    return decrease