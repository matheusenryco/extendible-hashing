def double_directory(self):
    """
    Doubles the directory size when necessary to accommodate new buckets.
    """
    
    new_refs = []
    for ref in self.directory.refs:
        new_refs.extend([ref] * 2)
        
    self.directory.refs = new_refs
    self.directory.dir_depth += 1