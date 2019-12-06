from tqdm import tqdm as tqdm
from IPython.core.display import HTML, display
from requests import session

## Get the list of semester ID (Works well)
url_all_the_semesters = "http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.filter?ww_b_list=1&ww_i_reportmodel=38507566&ww_c_langue=&ww_i_reportModelXsl=38510399&zz_x_PERIODE_ACAD=&ww_x_PERIODE_ACAD=1866894985&ww_x_NOM=&zz_x_TYPE_ROLE=&ww_x_TYPE_ROLE=null&zz_x_SESSION=&ww_x_SESSION=null&dummy=ok"
ww_x_PERS=[]
with session() as c:
    response = c.get(url_all_the_semesters)
    page_splits = response.text.split("ww_x_PERS=")[2:-1] #6:7 have already some datas. Full list at 2:-1
    for split in tqdm(page_splits):
        ww_x_PERS.append(split[:split.index("'")])

## Page saving as .xls
url_semester = "http://isa.epfl.ch/imoniteur_ISAP/!GEDPUBLICREPORTS.XLS?ww_x_TYPE_ROLE=null&ww_i_reportModel=38507566&ww_x_NOM=null&ww_x_PERS={}&ww_x_SESSION=null&ww_x_PERIODE_ACAD=1866894985&ww_i_reportModelXsl={}"
with session() as c:
    for ID in tqdm(ww_x_PERS):
            response = c.get(url_semester.format(ID,'38507597')) #38507597 is for Liste des inscrits (xls) (with sciper) and 38510399 is for Tableau des inscrits (xls) (no sciper but nice layout)
            with open('inscriptions_aux_examens_par_enseignants_'+ID+'.xls', 'w') as f:
                f.write(response.text)
