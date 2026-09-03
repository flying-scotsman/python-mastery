import csv
import collections

def read_csv_as_dicts(path, coltypes):
    with open(path, 'r') as f:
        data = csv.reader(f)
        header = next(data)
        rows = []
        for line in data:
            rows.append({name: func(val) for name, func, val in zip(header, coltypes, line)})
        return rows

def read_csv_as_columns(path, types):
    with open(path, 'r') as f:
        data = csv.reader(f)
        header = next(data)
        records = DataCollection(header)
        for line in data:
            records.append({name: func(val) for name, func, val in zip(header, types, line)})
        return records

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