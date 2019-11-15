import csv
import json
import pickle
from html.parser import HTMLParser

import tqdm
from IPython.core.display import HTML, display


class Element:
    def __init__(self, tag, parent):
        self.tag = tag
        self.parent = parent
        self.content = []
        self.data = []

    def html(self, ind=0):
        if self.content:
            t = '{}<{}>\n'.format(' ' * ind, self.tag)
            for d in self.data:
                t += '{}    {}\n'.format(' ' * ind, d)
            for c in self.content:
                t += '{}\n'.format(c.html(ind + 4))
            t += '{}</{}>'.format(' ' * ind, self.tag)
        else:
            data = self.data
            if len(data) == 0:
                data = ''
            if len(data) == 1:
                data = data[0]
            t = '{}<{}>{}</{}>'.format(' ' * ind, self.tag, data, self.tag)
        return t

    def __repr__(self):
        return self.html()

    def hastag(self, tag):
        for c in self.content:
            if c.tag == tag or c.hastag(tag):
                return True
        return False

    def __getitem__(self, i):
        return self.content[i]

    def __len__(self):
        return len(self.content)

    def __iter__(self):
        return iter(self.content)


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = Element("html", None)
        self.current = self.root
        self.tags = ['table', 'tr', 'td', 'th']

    def handle_starttag(self, tag, attrs):
        if tag in self.tags:
            el = Element(tag, self.current)
            self.current.content.append(el)
            self.current = el

    def handle_endtag(self, tag):
        if tag in self.tags:
            assert self.current.tag == tag
            self.current = self.current.parent

    def handle_data(self, data):
        if self.current.tag in self.tags:
            data = data.strip()
            if data:
                self.current.data.append(data)


def parse(html):
    parser = Parser()
    parser.feed(html)
    if len(parser.root) == 0:
        return []
    assert len(parser.root) == 1, parser.root
    main = parser.root.content[0]

    course = None
    teacher = None
    assistant = None
    label = None

    students = []

    for line in main:
        assert line.tag == 'tr'

        if line.hastag('th'):
            assert len(line) == 2

            assert len(line[0].data) == 1
            course = line[0].data[0]

            text = line[1].data
            if len(text) == 3:
                text = text[1:]

            assert len(text) <= 2, line
            if len(text) == 0:
                teacher, assistant = "", ""
            if len(text) == 1:
                teacher, assistant = text[0], ""
            if len(text) == 2:
                teacher, assistant = text

            if teacher.startswith('Enseignant-e-(s): '):
                teacher = teacher[len('Enseignant-e-(s): '):]
            if assistant.startswith('Assistant-e-(s): '):
                assistant = assistant[len('Assistant-e-(s): '):]
            continue

        if line.hastag('table'):
            if label is not None:
                assert course is not None and teacher is not None and assistant is not None
                assert len(line) == 1
                assert len(line[0]) == 1
                table = line[0][0]
                assert table.tag == 'table'
                for st in table:
                    assert st.tag == 'tr', table
                    assert len(st) == 4, table
                    st = [" ".join(x.data) for x in st] + [label, course, teacher, assistant]
                    students.append(st)
                label = None
            continue

        if line.hastag('td') and line[0].data:
            assert len(line) == 1
            if not 'ét.)' in line[0].data[0]:
                label = line[0].data[0]
            continue

    return students


with open('raw.pkl', 'rb') as f:
    periods = pickle.load(f)

with open('raw.pkl', 'rb') as f:
    periods = pickle.load(f)

for (year, season), htmls in tqdm.tqdm(periods.items()):
    students = []
    for html in tqdm.tqdm(htmls):
        students += parse(html)

    with open("data{}{}.csv".format(year, season), 'w') as f:
        writer = csv.writer(f)
        for st in students:
            writer.writerow(st)
