import sqlite3
from sqlite3.dbapi2 import Error
import traceback

CAR_TABLE = f"""CREATE TABLE CAR (
            CAR_URL VARCHAR(40) PRIMARY KEY NOT NULL,
            NOME VARCHAR(40) NOT NULL,
            PREZZO INT NOT NULL,
            IMG_URL VARCHAR(40),
            DATE VARCHAR(12),
            EURO INT NOT NULL,
            KM INT,
            DESCRIPTION VARCHAR(200)
        )"""

def getAllUrls(file:str)->set:
    con = None
    try:
        con = sqlite3.connect(file)
        cur = con.cursor()
        cur.execute(f"""SELECT CAR_URL FROM CAR""")
                        # WHERE PREZZO = (SELECT MIN(PREZZO) FROM CAR)
        carUrls = set()
        for url in cur.fetchall():
            carUrls.add(url[0])
        return carUrls
    except Error:
        traceback.print_exc()
    finally:
        if con:
            con.close()

def createTable(file):
    con = None
    try:
        con = sqlite3.connect(file)
        cur = con.cursor()
        cur.execute(CAR_TABLE)
        return
    except Error:
        traceback.print_exc()
    finally:
        if con:
            con.close()


def numElem(file):
    con = None
    try:
        con = sqlite3.connect(file)
        cur = con.cursor()
        cur.execute(f"""SELECT COUNT(*) FROM CAR""")
        return cur.fetchall()
    except Error:
        traceback.print_exc()
    finally:
        if con:
            con.close()


def lowestPrice(file):
    con=None
    try:
        con = sqlite3.connect(file)
        cur = con.cursor()
        cur.execute(f"""SELECT NOME,PREZZO,EURO,CAR_URL FROM CAR 
                        WHERE (PREZZO<3000 OR PREZZO is NULL)and (KM<110000 or KM is NULL) and (EURO>3 OR EURO is NULL)""")
                        # WHERE PREZZO = (SELECT MIN(PREZZO) FROM CAR)
        return cur.fetchall()
    except Error:
        traceback.print_exc()
    finally:
        if con:
            con.close()