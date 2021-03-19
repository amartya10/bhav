from datetime import datetime,timedelta
from io import BytesIO
import logging
import json
import requests as req 
from redis import Redis
import rejson as rej
import pandas as pd
from zipfile import ZipFile
DATE_FORMAT = "%d%m%y"
KEY_FORMAT = 'BSE:BHAV:EQ:'
client = rej.Client(host='localhost', port=6379, decode_responses=True)

def latest():
	date = datetime.today()
	# get latest date
	# not checkign for holidays
	if date.weekday() == 6:
		return  date - timedelta(days=2)
	if date.weekday() == 5:
		return  date - timedelta(days=1)
	if date.hour < 18:
		if date.weekday() == 0:
			return date - timedelta(days=3)
		return  date - timedelta(days=1)
	return date

def load_zip(file_name):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	base_url = "https://www.bseindia.com/download/BhavCopy/Equity/"
	req_url = f'{base_url}EQ{file_name}_CSV.ZIP'
	resp = req.get(req_url,headers=headers)
	resp.raise_for_status()
	return resp.content

def save(date = latest()):
	date =  date.strftime(DATE_FORMAT)
	if not client.exists(f'{KEY_FORMAT}{date}') : 
		_save(date)

def _save(date_str):
	try :
		resp_data = load_zip(date_str)
		if (resp_data) :
			zip_file = ZipFile(BytesIO(resp_data))
			csv_file = zip_file.open(f'EQ{date_str}.CSV')
			dfrm = pd.read_csv(csv_file)
			json = dfrm.to_json(orient =  "records")
			client.jsonset(f'{KEY_FORMAT}{date_str}',rej.Path.rootPath(),json)
	except Exception as ex:
		#TODO:HANDLER FILE AND URL NOT FOUND
		logging.warn(ex)

def get(date =  latest()):
	date_str = date.strftime(DATE_FORMAT)
	key  = f'{KEY_FORMAT}{date_str}'
	if not  client.exists(key):
		_save(date_str)
	dict_obejct = json.loads(client.jsonget(key,rej.Path.rootPath()))
	return dict_obejct

# def get_normalize(date = latest()):
#     date_str = date.strftime(DATE_FORMAT)
#     key =  f'BSE:EQ:DATE:{date_str}'
#     if  not client.exists(key):
#         _save_normalize(date)

#     key = f'BSE:EQ:DATE:{date_str}'
#     scripts = client.smembers(key)
#     equities = []
#     for script in scripts:
#         equities = []
#         sc_key =  f'BSE:EQ:CODE:{script}'
#         sc_date_key = f'{sc_key}DATE:{date_str}'
#         sc_info = client.hgetall(sc_key)    
#         sc_date_data = client.hgetall(sc) 
#         sc =  {**sc_info,**sc_date_data}
#         equities.append(sc)
    
#     return equities


# def _save_row(row,date_str):
#     print(row)
#     sc_key = f'BSE:EQ:CODE:{row.SC_CODE}'
#     if not client.exists(sc_key):
#         sc_info_data = {
#         'name':row.SC_NAME,
#         'type':row.SC_TYPE,
#         'code':row.SC_CODE,
#         }
#         client.hmset(sc_key,sc_info_data)
#     sc_date_data_key = f'{sc_key}:DATE:{date_str}'

#     if not client.exists(sc_date_key):
#         sc_date_data = {
#             'open':row.OPEN,
#             'high':row.HIGH,
#             'close':row.CLOSE,
#             'prevclose':row.PREVCLOSE,
#             'turnover':row.NET_TURNOV,
#             'shares':row.NO_OF_SHRS,
#             'trades':row.NO_TRADES,
#             'low':row.LOW,
#             'last':row.LAST,
#             'group':row.SC_GROUP,
#         }
#         sc_date_key =f'BSE:EQ:DATE:{date_str}'
#         client.sadd(sc_date_key,sc_key)
#         client.hmset(sc_date_data_key,sc_date_data)

# def _save_normalize(date_str):
#     print (date_str)
#     try :
#         resp_data = load_zip(date_str)
#         if (resp_data) :
#             zip_file = ZipFile(BytesIO(resp_data))
#             csv_file = zip_file.open(f'EQ{date_str}.CSV')
#             dfrm = pd.read_csv(csv_file)
#             for row in dfrm.iterrows():
#                 _save_row(row,date_str) 
#     except Exception as ex:
#         logging.info("exception loading file")

# def _save_as_string(date_str):
#     try :
#         resp_data = load_zip(date_str)
#         if (resp_data) :
#             zip_file = ZipFile(BytesIO(resp_data))
#             csv_file = zip_file.open(f'EQ{date_str}.CSV')
#             dfrm = pd.read_csv(csv_file)
#             json = dfrm.to_json(orient =  "records")
#             client.set(f'{KEY_FORMAT}{date_str}',json.dumps())
#     except Exception as ex:
#         pass
"""
"SC_CODE"     :CHAR,
"SC_NAME"    :CHAR,
"SC_GROUP"   :CHAR,
"SC_TYPE"    :CHAR,
"OPEN"       :FLOAT,
"HIGH"       :FLOAT,
"LOW"        :FLOAT,
"CLOSE"      :FLOAT,
"LAST"       :FLOAT,
"PREVCLOSE"  :FLOAT,
"NO_TRADES"  :INT,
"NO_OF_SHRS" :INT,
"NET_TURNOV" :FLOAT,
"TDCLOINDI"  :NULL
"""