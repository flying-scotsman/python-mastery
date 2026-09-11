import sys
import inspect

class Structure:
    @classmethod
    def set_fields(cls):
        cls._fields = tuple(inspect.signature(cls).parameters)

    @staticmethod
    def _init():
        locs = sys._getframe(1).f_locals
        self = locs['self']
        for name, val in locs.items():
            if name == 'self': continue
            setattr(self, name, val)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__,
                           ', '.join(repr(getattr(self, name)) for name in self._fields))

    def __setattr__(self, name, val):
        if name not in self._fields and not name.startswith("_"):
            raise AttributeError(f'No attribute {name}')
        super().__setattr__(name, val) # Super sets it on object, otherwise we recurse!
