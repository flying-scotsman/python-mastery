import inspect
import types
from typing import Callable
from functools import wraps
import decimal

class Validator:
    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, cls, name):
        self.name = name

    @classmethod
    def check(cls, value):
        return value

    def __set__(self, instance,	value):
        instance.__dict__[self.name] = self.check(value)

    # Collect all derived classes into a dict
    validators = { }
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.validators[cls.__name__] = cls
    

class Typed(Validator):
    expected_type = object
    @classmethod
    def check(cls, value):
        if not isinstance(value, cls.expected_type):
            raise TypeError(f'Expected {cls.expected_type}')
        return super().check(value)

class Positive(Validator):
    @classmethod
    def check(cls, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        return super().check(value)

class NonEmpty(Validator):
    @classmethod
    def check(cls, value):
        if len(value) == 0:
            raise ValueError('Must be non-empty')
        return super().check(value)

_typed_classes = [
    ('Integer', int),
    ('Float', float),
    ('Complex', complex),
    ('Decimal', decimal.Decimal),
    ('List', list),
    ('Bool', bool),
    ('String', str) ]

globals().update((name, type(name, (Typed,), {'expected_type':ty}))
                 for name, ty in _typed_classes)

class PositiveInteger(Integer, Positive):
    pass

class PositiveFloat(Float, Positive):
    pass

class NonEmptyString(String, NonEmpty):
    pass

def validated(func: Callable[...]):
    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = inspect.signature(func).bind(*args, **kwargs)
        errors = []
        for name, val in inspect.get_annotations(func).items():
            if name != 'return':
                try:
                    val.check(bound.arguments[name])
                except TypeError as e:
                    errors.append(f"{name}: {str(e)}")
        if len(errors) > 0:
            raise TypeError('Bad Arguments\n' + '\n'.join(errors))
        print('Calling', func.__name__)
        return func(*args, **kwargs)
    return wrapper
    
    
    for name, val in self.annotations.items():
        val.check(bound.arguments[name])

    print('Calling', self.func)
    result = self.func(*args, **kwargs)
    return result

def enforce(**types):
    errors = []
    return_type = types.pop('return_', None)
    def validator(func: Callable[...]):
        sig = inspect.signature(func)
        @wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            print(bound.arguments)
            for name, val in types.items():
                try:
                    print(f"Checking {bound.arguments[name]} is of type {val}")
                    val.check(bound.arguments[name])
                except TypeError as e:
                    errors.append(f"{name}: {str(e)}")
            if len(errors) > 0:
                raise TypeError('Bad Arguments\n' + '\n'.join(errors))
            result = func(*args, **kwargs)

            # Now check that the result is of the correct type
            return_type.check(result)

            return result
        return wrapper
    return validator


class ValidatedFunction:
    def __init__(self, func):
        self.func = func
        self.signature = inspect.signature(func)
        self.annotations = inspect.get_annotations(func)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return types.MethodType(self, instance)

    def __call__(self, *args, **kwargs):
        bound = self.signature.bind(*args, **kwargs)

        for name, val in self.annotations.items():
            val.check(bound.arguments[name])

        print('Calling', self.func)
        result = self.func(*args, **kwargs)
        return result

class Stock:
    name   = String()
    shares = PositiveInteger()
    price  = PositiveFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def __repr__(self):
        return f"Stock('{self.name}', {self.shares}, {self.price})"

    def __eq__(self, other):
        return isinstance(other, Stock) and ((self.name, self.shares, self.price) == 
                                             (other.name, other.shares, other.price))

    @property
    def cost(self):
        return self.shares * self.price

    # @property
    # def shares(self):
    #     return self._shares

    # @shares.setter
    # def shares(self, value):
    #     self._shares = PositiveInteger.check(value)

    # @property
    # def price(self):
    #     return self._price

    # @price.setter
    # def price(self, value):        
    #     self._price = PositiveFloat.check(value)

    @validated
    def sell(self, nshares: Integer):
        self.shares -= nshares
        # TODO: What about negative values?

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)

    sell = ValidatedFunction(sell)
