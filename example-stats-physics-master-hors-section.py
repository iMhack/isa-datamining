import pandas as pd
import zipfile
import io 
import csv
from IPython.display import display, HTML
from tqdm.notebook import tqdm
c = []
with zipfile.ZipFile('data2012_2019.zip','r') as zf:
    for e in zf.namelist():
        c.append([row for row in csv.reader(io.TextIOWrapper(zf.open(e, 'r'), encoding='utf-8'))])
        
for semester in c:#The section is not written at entry 2 if it is the same as entry 6.
    for entry in semester:
        if not entry[2]:
            entry[2] = entry[6]

hors_section = [[entry for entry in semester
                 if entry[2] != entry[6] and "hysique" in entry[2] and "Master" in entry[2] and not "hysique" in entry[6] and not "Programme" in entry[6]]
                for semester in c]

nom_cours_semester = [{entry[3] for entry in semester} for semester in hors_section]
dataz = [
    sorted([
        (len([
            None for entry in sem_entry_hors_section if entry[3] == course_name
        ]), course_name, 
         {entry[6] for entry in sem_entry_hors_section if entry[3] == course_name},
        [entry[4] for entry in sem_entry_hors_section if entry[3] == course_name][0]) 
        for course_name in sem_course_name
    ], reverse=True)  for sem_course_name, sem_entry_hors_section in zip(nom_cours_semester, hors_section)
]

with pd.ExcelWriter('stats_physique_master_hors_section.xlsx', engine='xlsxwriter') as writer:
        for e,d in zip(zf.namelist(), dataz):
            pd.DataFrame(d).to_excel(writer, sheet_name=e, index=False, header=False)
