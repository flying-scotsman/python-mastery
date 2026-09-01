import csv
from collections import defaultdict
import readrides
from pprint import pprint

# A function that reads a file into a list of dicts
def read_portfolio(filename):
    portfolio = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            record = {
                'name' : row[0],
                'shares' : int(row[1]),
                'price' : float(row[2])
            }
            portfolio.append(record)
    return portfolio

rows = readrides.read_rides_as_dict('Data/ctabus.csv')

def number_of_bus_routes(rides: list) -> int:
    return len({ride['route'] for ride in rides})

def footfall(bus_route: int, date: str, rides: list) -> int:
    # Somehow this isn't working - not getting any hits on 22, February 2 2011
    for ride in rides:
        if ride['date'] == date:
            return ride['rides']

def total_rides_per_route(rides: list) -> int:
    # routes = {ride['route'] for ride in rides}
    total_rides = defaultdict(int)
    # Iterate through all rides and add number of rides to dict entry
    for ride in rides:
        total_rides[ride['route']] += ride['rides']
    pprint(sorted(total_rides.items(), key = lambda x: x[1]))

def largest_increase_ridership(rides: list, start = '2001', end = '2011'):
    # Add up all the rides for all routes in given years
    total_rides = defaultdict(lambda: defaultdict(int)) # Nested by route then year
    for ride in rides:
        for date in (start, end):
            if date in ride['date']:
                total_rides[ride['route']][date] += ride['rides']
    differences = sorted({k: v[end] - v[start] for k, v in total_rides.items()}.items(), key = lambda x: x[1])[-5:]
    print(differences)

largest_increase_ridership(rows)