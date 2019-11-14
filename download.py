import os
import pickle
import urllib.error
import urllib.parse
import urllib.request
from itertools import count
import pandas as pd
import requests
from tqdm import tqdm as tqdm
from io import StringIO

url_base = "https://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.filter?" \
    + "ww_b_list={}&ww_i_reportmodel={}&ww_c_langue={}&ww_i_reportModelXsl={}&" \
    + "ww_x_CLASSE={}&ww_x_PERIODE_ACAD={}&ww_x_HIVERETE={}&ww_x_MATIERE={}"

url_course = "https://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.{}?" \
    + "ww_x_MAT={}&ww_x_CLASSE={}&ww_i_reportmodel={}&ww_x_MATIERE={}&" \
    + "ww_x_PERIODE_ACAD={}&ww_i_reportModelXsl={}&ww_x_HIVERETE={}"


ww_b_list = ["1"]
ww_i_reportmodel = ["66627699"]
ww_c_langue = [""]
ww_i_reportModelXsl = ["66627723", "66627727"] #htlm, xls
page_type = ["HTML","XLS"] #choos with pt variable
ww_x_CLASSE = ["null"]
ww_x_PERIODE_ACAD = ["123456101", "213637754", "213637922", "213638028", "355925344", "355925344", "1866893861", "1866894985"]
ww_x_PERIODE_ACAD = list(zip(ww_x_PERIODE_ACAD, count(2012)))
ww_x_HIVERETE = [("2936286", "autumn"), ("2936295", "spring")]
ww_x_MATIERE = ["*"]

pt=1
save_xls=True
periods = dict()

if os.path.isfile('raw.pkl'):
    with open('raw.pkl', 'rb') as f:
        periods = pickle.load(f)

for year, year_name in tqdm(ww_x_PERIODE_ACAD):
    for season, season_name in tqdm(ww_x_HIVERETE):
        key = (year_name, season_name)
        print(key)
        if key in periods:
            continue

        url_list = url_base.format(ww_b_list[0], ww_i_reportmodel[0], ww_c_langue[0],  ww_i_reportModelXsl[0],
                                      ww_x_CLASSE[0], year, season, ww_x_MATIERE[0])
        print(url_list)
        response = urllib.request.urlopen(url_list)
        webContent = str(response.read(), 'latin1')
        page_splits = webContent.split("ww_x_MAT=")[1:-1]

        xs = []

        for k, split in enumerate(tqdm(page_splits)):
            ww_x_MAT = [split[:split.index("'")]]
            url_mat = url_course.format(page_type[pt], ww_x_MAT[0], ww_x_CLASSE[0], ww_i_reportmodel[0], ww_x_MATIERE[0],
                             year, ww_i_reportModelXsl[pt], season)
            print("  {}".format(url_mat))
            response = requests.get(url_mat)
            if pt == 1:
                if save_xls:
                    with open(''+str(key[0])+","+str(key[1])+","+str(ww_x_MAT[0])+'.xls', 'w') as f:
                        f.write(response.text)
                else:
                    try:
                        xs.append(pd.read_html(response.text))
                    except:
                        print("Can't parse")
            else:
                xs.append(response.text)

        periods[key] = xs

        with open('raw.pkl', 'wb') as f:
            pickle.dump(periods, f)
