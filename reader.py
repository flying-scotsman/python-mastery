import csv
from collections.abc import Iterable, Callable


def read_csv_as_dicts(filename: str, types: list[Callable[[str], object]]):
    '''
    Read CSV data into a list of dictionaries with optional type conversion
    '''
    with open(filename) as file:
        return csv_as_dicts(file, types)
    return []

def read_csv_as_instances[T](filename: str, cls: type[T]):
    '''
    Read CSV data into a list of instances
    '''
    with open(filename) as file:
        return csv_as_instances(file, cls)
    return []

def csv_as_dicts(file: Iterable[str], types: list[Callable[[str], object]], headers: list[str] = None):
    '''
    Read CSV data into a list of dictionaries with optional type conversion.

    Optionally accepts headers for headerless CSVs.
    '''
    records = []
    rows = csv.reader(file)
    if headers is None:
        headers = next(rows)
    for row in rows:
        record = { name: func(val) 
                   for name, func, val in zip(headers, types, row) }
        records.append(record)
    return records

def csv_as_instances[T](file: Iterable[str], cls: type[T], headers: list[str] = None):
    '''
    Read CSV data into a list of instances.

    Optionally accepts headers for headerless CSVs.
    '''
    records = []
    rows = csv.reader(file)
    if headers is None:
        headers = next(rows)
    for row in rows:
        record = cls.from_row(row)
        records.append(record)
    return records