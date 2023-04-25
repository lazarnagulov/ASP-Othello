class Pair(object):

    __slots__ = "key", "value"
    
    def __init__(self, key, value):
        self.key = key
        self.value = value
    
    def __hash__(self):
        pass
    
    def __str__(self):
        return self.key + ":" + self.value
    
class HashMap(object):
    
    def __init__(self, cap=11, p=109345121):
        self._n = 0
        self._prime = p
        self._table = cap * [ None ]
    
    def __getitem__(self):
        pass
    
    def __setitem__(self, value):
        pass
    
    def __delitem__(self, key):
        pass
    
    def __iter__(self):
        pass
    
    def __len__(self):
        pass
    
    def __contains__(self):
        pass
    
    def clear(self):
        self._table = []
        
    def update(self, key, value):
        pass
    
    def __eq__(self):
        pass
    
    def __neq__(self):
        pass
    