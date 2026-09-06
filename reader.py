import csv
import collections
from abc import ABC, abstractmethod

def read_csv_as_dicts(filename, coltypes):
    parser = DictCSVParser(coltypes)
    return parser.parse(filename)

def read_csv_as_columns(filename, types):
    with open(filename, 'r') as f:
        data = csv.reader(f)
        header = next(data)
        records = DataCollection(header)
        for line in data:
            records.append({name: func(val) for name, func, val in zip(header, types, line)})
        return records

def read_csv_as_instances(filename, cls):
    parser = InstanceCSVParser(cls)
    return parser.parse(filename)

class DataCollection(collections.abc.Sequence):
    def __init__(self, header):
        self.data = [] # Nested list
        self.columns = []
        for column in header:
            self.data.append([])
            self.columns.append(column)

    def __len__(self):
        # All lists assumed to have the same length
        try:
            return len(self.data[0])
        except IndexError:
            return 0

    def __getitem__(self, index):
        # if isinstance(index, slice):
        #     return [{'route': self.routes[i],
        #              'date': self.dates[i],
        #              'daytype': self.daytypes[i],
        #              'rides': self.numrides[i]} for i in range(index.start, index.stop)]
        return { column: self.data[i][index] for i, column in enumerate(self.columns)}

    def append(self, d):
        for data, column in zip(self.data, self.columns):
            data.append(d[column])

class CSVParser(ABC):

    def parse(self, filename):
        records = []
        with open(filename) as f:
            rows = csv.reader(f)
            headers = next(rows)
            for row in rows:
                record = self.make_record(headers, row)
                records.append(record)
        return records

    @abstractmethod
    def make_record(self, headers, row):
        pass

class DictCSVParser(CSVParser):
    def __init__(self, types):
        self.types = types

    def make_record(self, headers, row):
        return { name: func(val) for name, func, val in zip(headers, self.types, row) }

class InstanceCSVParser(CSVParser):
    def __init__(self, cls):
        self.cls = cls

    def make_record(self, headers, row):
        return self.cls.from_row(row)