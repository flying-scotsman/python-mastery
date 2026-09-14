import sys
import inspect

class Structure:
    @classmethod
    def create_init(cls):
        argstr = ','.join(cls._fields)
        code = f'def __init__(self, {argstr}):\n'
        for name in cls._fields:
            code += f'    self.{name} = {name}\n'
        locs = { }
        exec(code, locs)
        cls.__init__ = locs['__init__']

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__,
                           ', '.join(repr(getattr(self, name)) for name in self._fields))

    def __setattr__(self, name, val):
        if name not in self._fields and not name.startswith("_"):
            raise AttributeError(f'No attribute {name}')
        super().__setattr__(name, val) # Super sets it on object, otherwise we recurse!
