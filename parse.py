import csv
import json
import pickle
from html.parser import HTMLParser

from IPython.core.display import HTML, display
from tqdm import tqdm as tqdm


class ISA_HTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = []
        self.tables = []
        self.tr = None
        self.entry = None

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.tables.append([])  # start saving a table (you can have a table into another table)
        if tag == 'tr':
            self.tr = []  # start saving a line (you cannot have a line into another line)
        if tag in ['td', 'th']:
            self.entry = []  # start saving an entry (you cannot have an entry into another entry)

    def handle_endtag(self, tag):
        if tag == 'table' and self.tables:
            table = self.tables.pop()
            if table:  # don't save empty tables
                if self.tables:
                    self.tables[-1].append(table)
                else:  # root table
                    self.data.append(table)

        if tag == 'tr' and type(self.tr) == list:
            if self.tables:
                if self.tr:  # don't save empty lines
                    self.tables[-1].append(self.tr)
                self.tr = None
            else:
                print("tr outside a table: {}".format(self.tr))

        if tag in ['td', 'th'] and self.entry:
            if type(self.tr) == list:
                self.tr.append("\n".join(self.entry))
                self.entry = None
            else:
                print("td/th outside a tr: {}".format(self.td))

    def handle_data(self, data):
        if type(self.entry) is list:
            self.entry.append(data.strip())


def parse(raw):
    parser = ISA_HTMLParser()
    parser.feed(raw)

    if len(parser.data) == 0:
        return []

    main = parser.data[0]

    if len(main[0]) != 2:
        return []

    course, teacher = main[0]
    course = course.strip()

    if 'Enseignant' in teacher:
        teacher = teacher.split('Enseignant-e-(s):')[1]
        if 'Assistant-e-(s):' in teacher:
            teacher, assistant = teacher.split("Assistant-e-(s):")
        else:
            assistant = ""
        teacher = teacher.strip()
        assistant = assistant.strip()
    else:
        teacher = teacher.strip()
        assistant = ""

    students = []

    def fmt(x):
        if len(x) == 3:
            return x
        if len(x) < 3:
            return x + [""] * (3 - len(x))
        assert False, x

    def valid(x):
        if type(x[0]) is list:
            return False
        return True

    i = 1
    while i < len(main):
        if len(main[i]) == 1:
            label = main[i][0]
            i += 1

            if i >= len(main):
                break

            if 'ét' in main[i][0]:
                i += 1

                students += [fmt(x) + [course, teacher, assistant, label] for x in main[i] if valid(x)]
                i += 1
            else:
                i += 0
        else:
            i += 1

    return students


with open('raw.pkl', 'rb') as f:
    periods = pickle.load(f)

stop = False

for (year, season), xs in tqdm(periods.items()):
    students = []
    for html in tqdm(xs):
        try:
            students += parse(html)
        except:
            print(html)
            display(HTML(html))
            stop = True

        if stop:
            break
    if stop:
        break

    with open("data{}{}.csv".format(year, season), 'w') as f:
        writer = csv.writer(f)
        for x in students:
            writer.writerow(x)
