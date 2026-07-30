import csv
from functools import partial

def read_rides_as_tuples(filename):
    '''
    Read the bus ride data as a list of tuples
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = (route, date, daytype, rides)
            records.append(record)
    return records

def read_rides_as_dict(filename):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            record = dict()
            record['route'] = row[0]
            record['date'] = row[1]
            record['daytype'] = row[2]
            record['rides'] = int(row[3])
            records.append(record)
    return records

class RowClass:
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides

def read_rides_as_class(filename, class_type):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            record = class_type(*row)
            records.append(record)
    return records

from collections import namedtuple
RowNT = namedtuple('Row', ['route', 'date', 'daytype', 'rides'])

def read_rides_as_namedtuples(filename):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            record = RowNT(*row)
            records.append(record)
    return records

class RowSlottedClass:
    __slots__ = ['route', 'date', 'daytype', 'rides']
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides

if __name__ == '__main__':
    import tracemalloc
    functions = (read_rides_as_tuples, read_rides_as_dict, partial(read_rides_as_class, class_type=RowClass), read_rides_as_namedtuples, partial(read_rides_as_class, class_type=RowSlottedClass))
    for fn in functions:
        tracemalloc.start()
        rows = fn('Data/ctabus.csv')
        try:
            name = fn.__name__
        except AttributeError:
            name = fn.func.__name__
        print(f'Memory Use of {name}: Current {tracemalloc.get_traced_memory()[0]}, Peak {tracemalloc.get_traced_memory()[1]}')
        tracemalloc.stop()