class TableFormatter:
    def headings(self, headers):
        raise NotImplementedError()

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

def create_formatter(format: str):
    if format == 'text':
        return TextTableFormatter()
    elif format == 'csv':
        return CSVTableFormatter()
    elif format == 'html':
        return HTMLTableFormatter()
    return NotImplementedError

def print_table(records, fields, formatter):
    # print(' '.join('%10s' % fieldname for fieldname in fields))
    # print(('-'*10 + ' ')*len(fields))
    # for record in records:
    #     print(' '.join('%10s' % getattr(record, fieldname) for fieldname in fields))
    formatter.headings(fields)
    for r in records:
        rowdata = [getattr(r, fieldname) for fieldname in fields]
        formatter.row(rowdata)
