import inspect
import types

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

class Integer(Typed):
    expected_type = int

class Float(Typed):
    expected_type = float

class String(Typed):
    expected_type = str

class PositiveInteger(Integer, Positive):
    pass

class PositiveFloat(Float, Positive):
    pass

class NonEmptyString(String, NonEmpty):
    pass

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
        print(*args, **kwargs)
        bound = self.signature.bind(*args, **kwargs)

        for name, val in self.annotations.items():
            print(f"Checking that {bound.arguments[name]} is of type {val}")
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

    def sell(self, nshares: Integer):
        self.shares -= nshares
        # TODO: What about negative values?

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)

    sell = ValidatedFunction(sell)
