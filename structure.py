class Structure:
    def __init__(self, *args):
        # How can I populate instance variables using kwargs and _fields?
        # Answer: I use setattr
        if len(args) != len(self._fields):
            raise IndexError(f"Expected {len(self._fields)} arguments")
        for i, f in enumerate(self._fields):
            setattr(self, f, args[i])

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__,
                           ', '.join(repr(getattr(self, name)) for name in self._fields))

    def __setattr__(self, name, val):
        if name not in self._fields and not name.startswith("_"):
            raise AttributeError(f'No attribute {name}')
        super().__setattr__(name, val) # Super sets it on object, otherwise we recurse!
