import csv
from collections.abc import Iterable, Callable
from typing import Any
from functools import partial

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
    def make_dict(headers, types, row):
        return {name: func(val) for name, func, val in zip(headers, types, row)}
    func = partial(make_dict, types=types)
    return convert_csv(file, func)

def csv_as_instances[T](file: Iterable[str], cls: type[T], headers: list[str] = None):
    '''
    Read CSV data into a list of instances.

    Optionally accepts headers for headerless CSVs.
    '''
    def make_instance(row, cls, headers = None):
        return cls.from_row(row)
    func = partial(make_instance, cls=cls)
    return convert_csv(file, func)

def convert_csv(lines: Iterable[str], fn: Callable):
    # This function shouldn't accept headers as an argument
    # But how do we get the headers in then?
    records = []
    rows = csv.reader(lines)
    headers = next(rows)
    return list(map(lambda row: fn(headers=headers, row=row), rows))