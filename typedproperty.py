def typedproperty(name, expected_type):
    private_name = '_' + name

    @property
    def value(self):
        print(f"{private_name =}")
        return getattr(self, private_name)

    @value.setter
    def value(self, val):
        if not isinstance(val, expected_type):
            raise TypeError(f'Expected {expected_type}')
        setattr(self, private_name, val)

    return value

def String():
    return typedproperty("Name", str)

def Integer():
    return typedproperty("Integer", int)

def Float():
    return typedproperty("Price", float)

class Stock:
    name = String()
    shares = Integer()
    price = Float()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

