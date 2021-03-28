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
SC_KEY_FORMAT = 'BSE:BHAV:EQ:'

KEY_DATE_FORMAT ='BSE:BAHV:DATE'
SC_DATE_KEY_FORMAT =  ':DATE:'
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

def _save_row(row,date_str):
    sc_key = f'BSE:EQ:CODE:{row.SC_CODE}'
    if not client.exists(sc_key):
        sc_info_data = {
        'SC_NAME':row.SC_NAME,
        'SC_TYPE':row.SC_TYPE,
        'SC_CODE':row.SC_CODE,
        }
        client.hmset(sc_key,sc_info_data)
    sc_date_data_key = f'{sc_key}:DATE:{date_str}'

    if not client.exists(sc_date_data_key):
        sc_date_data = {
            'OPEN':row.OPEN,
            'HIGH':row.HIGH,
            'CLOSE':row.CLOSE,
            'PREVCLOSE':row.PREVCLOSE,
            'NET_TURNOV':row.NET_TURNOV,
            'NO_OF_SHRS':row.NO_OF_SHRS,
            'NO_TRADES':row.NO_TRADES,
            'LOW':row.LOW,
            'LAST':row.LAST,
            'SC_GROUP':row.SC_GROUP,
        }
        client.hmset(sc_date_data_key,sc_date_data)

    sc_date_key =f'BSE:EQ:DATE:{date_str}'
    client.sadd(sc_date_key,sc_key)


def _save(date_str):
    try:
        resp_data = load_zip(date_str)
        if resp_data:
            zip_file = ZipFile(BytesIO(resp_data))
            csv_file = zip_file.open(f'EQ{date_str}.CSV')
            dfrm = pd.read_csv(csv_file)
            for  row  in dfrm.itertuples():
                _save_row(row,date_str)
            #  lamda is better 
        else:
            raise Exception('resp not found')
    except Exception as e:
        raise e


def save(date = latest()):
    if isinstance(date,datetime):
        date = date.strftime(DATE_FORMAT)
    key = f'{KEY_DATE_FORMAT}:{date}'
    _save(date)


def get(date = latest()):

    # return [{'date':date}]
    date_str = date.strftime(DATE_FORMAT)
    key =  f'BSE:EQ:DATE:{date_str}'
    if  not client.exists(key):
        _save(date_str )

    scripts = client.smembers(key)
    equities = []
    for script in scripts:
        sc_date_key = f'{script}:DATE:{date_str}'
        sc_info = client.hgetall(script)    
        sc_date_data = client.hgetall(sc_date_key) 
        sc =  {**sc_info,**sc_date_data}
        equities.append(sc)    
    return equities


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