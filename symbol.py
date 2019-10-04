class Symbol:
    def __init__(self, name, symtype, value, padding=0):
        self.name = name
        self.type = symtype
        self.value = value
        self.padding = padding

    def __str__(self):
        return 'Symbol(name={}, type={}, value={}, padding={})'.format(self.name, self.type, self.value, self.padding)
    
    def __repr__(self):
        return 'Symbol(name={}, type={}, value={}, padding={})'.format(self.name, self.type, self.value, self.padding)