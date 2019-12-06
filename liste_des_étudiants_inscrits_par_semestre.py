from tqdm import tqdm as tqdm
from IPython.core.display import HTML, display
from requests import session

## Get the list of semester ID (Works well)
url_all_the_semesters = "http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.filter?ww_b_list=1&ww_i_reportmodel=133685247&ww_c_langue=&ww_i_reportModelXsl=133685270&zz_x_UNITE_ACAD=&ww_x_UNITE_ACAD=null&zz_x_PERIODE_ACAD=&ww_x_PERIODE_ACAD=null&zz_x_PERIODE_PEDAGO=&ww_x_PERIODE_PEDAGO=null&zz_x_HIVERETE=&ww_x_HIVERETE=null&dummy=ok"
ww_x_GPS=[]
with session() as c:
    response = c.get(url_all_the_semesters)
    page_splits = response.text.split("ww_x_GPS=")[2:-1] #6:7 have already some datas. Full list at 2:-1
    for split in tqdm(page_splits):
        ww_x_GPS.append(split[:split.index("'")])

## Page saving as .xls
url_semester = "https://isa.epfl.ch/imoniteur_ISAP/!GEDREPORTS.html?ww_x_PERIODE_PEDAGO=null&ww_x_UNITE_ACAD=null&ww_i_reportModel=133685247&ww_x_GPS={}&ww_x_PERIODE_ACAD=null&ww_i_reportModelXsl={}&ww_x_HIVERETE=null"
login_url = 'https://isa.epfl.ch/imoniteur_ISAP/!logins.tryToConnect'        

payload = {
    'ww_x_username': 'user',
    'ww_x_password': 'password'
}
with session() as c:
    c.post(login_url, data=payload)
    for ID in tqdm(ww_x_GPS):
            if not 'ISA-CNXKEY' in [cookie.name for cookie in c.cookies]:
                raise ValueError("Issue while connecting with login={}, password={}".format(payload['ww_x_username'], payload['ww_x_password']))
            response = c.get(url_semester.format(ID,'133685271')) #133685270 is html, 133685271 is xls
            if response.text.find('Statut') != -1:#Not empty
                display(HTML(response.text))
                with open(ID+'.xls', 'w') as f:
                    f.write(response.text)
