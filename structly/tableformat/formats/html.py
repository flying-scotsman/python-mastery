from ..formatter import TableFormatter

class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        print("<tr> " + "".join("<th>%s</th>" % h for h in headers) + " </tr>")

    def row(self, rowdata):
        print("<tr> " + "".join("<th>%s</th>" % str(d) for d in rowdata) + " </tr>")