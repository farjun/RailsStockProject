import requests
import sqlite3
import sys


def connect():
    database = sqlite3.connect('testDatabase.db',isolation_level=None,timeout=10)
    return database

def fetch_stock(symbol):
    url = "https://sandbox.iexapis.com/stable/stock/"+str(symbol)+"/quote?token=Tpk_087a52e2547e449e9cee8748f00491eb"
    response=requests.get(url)
    if (response.status_code)==404:
        return 0
    else:
        dataset = response.json()
    return (dataset)

def is_cached(ssymbol,database):
    c1 = database.cursor()
    res = list(c1.execute('''select symbol from stocks '''))
    res=flatter(res)
    if ssymbol in res:
        return True
    else:
        return False

def add_stock_to_db(symbol,database):
    if is_cached(symbol.upper(),database) is True:

        sys.exit()
    else:
        stock_data=fetch_stock(symbol)
        if stock_data==0:
            exit(0)
        else :
            c1 = database.cursor()
            c1.execute("INSERT INTO stocks VALUES (?,?)", [stock_data["symbol"], stock_data["companyName"]])

def flatter(tu):
    l = []
    for i in tu:
        l.append(i[0])
    return l


stocksDatabase=connect()
add_stock_to_db('gold',stocksDatabase)