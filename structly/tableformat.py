from abc import ABC, abstractmethod

class TableFormatter(ABC):
    @abstractmethod
    def headings(self, headers):
        raise NotImplementedError()

    @abstractmethod
    def row(self, rowdata):
        raise NotImplementedError()

class TextTableFormatter(TableFormatter):
    def headings(self, headers):
        print(' '.join('%10s' % h for h in headers))
        print(('-'*10 + ' ')*len(headers))
    
    def row(self, rowdata):
        print(' '.join('%10s' % d for d in rowdata))

class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        print(",".join(headers))

    def row(self, rowdata):
        print(",".join([str(d) for d in rowdata]))

class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        print("<tr> " + "".join("<th>%s</th>" % h for h in headers) + " </tr>")

    def row(self, rowdata):
        print("<tr> " + "".join("<th>%s</th>" % str(d) for d in rowdata) + " </tr>")

def create_formatter(format: str, column_formats: list | None = None, upper_headers: bool | None = None):
    if format == 'text':
        formatter_cls = TextTableFormatter
    elif format == 'csv':
        formatter_cls = CSVTableFormatter
    elif format == 'html':
        formatter_cls = HTMLTableFormatter
    else:
        return NotImplementedError

    if column_formats is not None:
        class formatter_cls(ColumnFormatMixin, formatter_cls):
            formats = column_formats
    if upper_headers:
        class formatter_cls(UpperHeadersMixin, formatter_cls):
            pass

    return formatter_cls()

def print_table(records, fields, formatter):
    if not isinstance(formatter, TableFormatter):
        return TypeError("Expected a TableFormatter")
    formatter.headings(fields)
    for r in records:
        rowdata = [getattr(r, fieldname) for fieldname in fields]
        formatter.row(rowdata)

class ColumnFormatMixin:
    formats = []
    def row(self, rowdata):
        rowdata = [(fmt % d) for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)

class UpperHeadersMixin:
    def headings(self, headers):
        super().headings([h.upper() for h in headers])