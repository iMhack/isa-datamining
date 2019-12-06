# isa-datamining

Small tool to get datas publicly available on is-academia websites.

### inscriptions_aux_cours_par_matières.py
This is downloading datas that are here : https://isa.epfl.ch/imoniteur_ISAP/%21gedpublicreports.htm?ww_i_reportmodel=66627699
One can download the .xml or the .html pages (a bit messy). With .html pages, one could then parse them with parse.py
### liste_des_étudiants_inscrits_par_semestre.py
This is downloading datas that are here : http://isa.epfl.ch/imoniteur_ISAP/%21gedpublicreports.htm?ww_i_reportmodel=133685247
One can give login+password to get Nationality. The data are saved as .xml (html xml style).
One can read them as all_the_datas = [pd.read_html(fn, header=2) for fn in os.listdir(os.getcwd()+'/data_login2') if pd.read_html(fn, header=2)!=[]]
### Liste des inscriptions aux examens par enseignants
This is downloading datas that are here : http://isa.epfl.ch/imoniteur_ISAP/%21gedpublicreports.htm?ww_i_reportmodel=38507566
login+password don't give anything more
