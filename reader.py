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
    return convert_csv(file, lambda headers, row: {name: func(val) for name, func, val in zip(headers, types, row)})

def csv_as_instances[T](file: Iterable[str], cls: type[T], headers: list[str] = None):
    '''
    Read CSV data into a list of instances.

    Optionally accepts headers for headerless CSVs.
    '''
    return convert_csv(file, lambda _, row: cls.from_row(row))

def convert_csv(lines: Iterable[str], fn: Callable):
    # This function shouldn't accept headers as an argument
    # But how do we get the headers in then?
    records = []
    rows = csv.reader(lines)
    headers = next(rows)
    return list(map(lambda row: fn(headers, row), rows))