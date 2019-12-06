# isa-datamining

Small tool to get datas publicly available on is-academia websites.

Naming is not consistant but...
### download.py
This is downloading datas that are here : https://isa.epfl.ch/imoniteur_ISAP/%21gedpublicreports.htm?ww_i_reportmodel=66627699
One can download the .xml or the .html pages (a bit messy). With .html pages, one could then parse them with parse.py
### get-semester-login.py
This is downloading datas that are here : http://isa.epfl.ch/imoniteur_ISAP/%21gedpublicreports.htm?ww_i_reportmodel=133685247
One can give login+password to get Nationality. The data are saved as .xml (html xml style).
One can read them as all_the_datas = [pd.read_html(fn, header=2) for fn in os.listdir(os.getcwd()+'/data_login2') if pd.read_html(fn, header=2)!=[]]
