import csv

class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares
        # TODO: What about negative values?

def read_portfolio(filename):
    with open(filename, 'r') as f:
        data = csv.reader(f)
        header = next(data)
        stocks = [Stock(*row) for row in data]
        return stocks

def print_portfolio(portfolio):
    print('%10s %10s %10s' % ('name', 'shares', 'price'))
    print('-'*10, '-'*10, '-'*10)
    for s in portfolio:
        print('%10s %10s %10s' % (s.name, s.shares, s.price))