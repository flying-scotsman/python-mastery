class Stock:
    _types = (str, int, float)
    __slots__ = ['name', '_shares', '_price']

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @property
    def cost(self):
        return self.shares * self.price

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        if not isinstance(value, self._types[1]):
            raise TypeError(f"Expected {self._types[1]}")
        elif value < 0:
            raise ValueError("shares must be >= 0")

        self._shares = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, self._types[2]):
            raise TypeError(f"Expected {self._types[2]}")
        elif value < 0:
            raise ValueError("price must be >= 0")
        
        self._price = value

    def sell(self, nshares):
        self._shares -= nshares
        # TODO: What about negative values?

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)

def print_portfolio(portfolio):
    print('%10s %10s %10s' % ('name', 'shares', 'price'))
    print('-'*10, '-'*10, '-'*10)
    for s in portfolio:
        print('%10s %10s %10s' % (s.name, s.shares, s.price))