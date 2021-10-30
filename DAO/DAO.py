import sqlite3
from sqlite3.dbapi2 import Connection, Error
import traceback
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from models.Car import Car
DB_PATH =".\car.db"

CAR_TABLE = f"""CREATE TABLE CAR (
            CAR_URL VARCHAR(40) PRIMARY KEY NOT NULL,
            NOME VARCHAR(40) NOT NULL,
            PREZZO INT NOT NULL,
            IMG_URL VARCHAR(40),
            DATE VARCHAR(12),
            EURO INT,
            KM INT,
            DESCRIPTION VARCHAR(200),
            EXPIRED BOOLEAN NOT NULL DEFAULT 0,
            CREATION_DATE DATE NOT NULL
        )"""


def checkExpiredAndUpdate(con:Connection):
    pass


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
        print("ERROR")
        traceback.print_exc()
    finally:
        if con:
            con.close()

def getAllCars(file:str)->list:
    con = None
    try:
        con = sqlite3.connect(file)
        cur = con.cursor()
        cur.execute(f"""SELECT CAR_URL,NOME,PREZZO,IMG_URL,DATE,EURO,KM,DESCRIPTION,CREATION_DATE,EXPIRED FROM CAR""")
        cars = []
        for car in cur.fetchall():
            expired = 1
            if car[9] == 1:
                expired = True
            else: expired = False
            cars.append(Car(car[1],car[2],car[0],car[3],car[4],car[5],car[6],car[7],car[8],expired))
        return cars

    except Error:
        traceback.print_exc()
    finally:
        if con:
            con.close()

def createTable(file:str):
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


def numElem(file:str):
    con = None
    try:
        con = sqlite3.connect(file)
        cur = con.cursor()
        cur.execute(f"""SELECT COUNT(*) FROM CAR""")
        return cur.fetchall()[0][0]
    except Error:
        traceback.print_exc()
    finally:
        if con:
            con.close()

def saveAll(cars, file:str):
    con = None
    try:
        con = sqlite3.connect(file)
        for car in cars:
            car.saveToDb(con)
        return 
    except Error:
        traceback.print_exc()
    finally:
        if con:
            con.close()

def lowestPrice(file:str):
    con=None
    try:
        con = sqlite3.connect(file)
        cur = con.cursor()
        cur.execute(f"""SELECT NOME,PREZZO,EURO,CAR_URL,EXPIRED FROM CAR 
                        WHERE (PREZZO<3000 OR PREZZO is NULL)and (KM<110000 or KM is NULL) and (EURO>3 OR EURO is NULL)""")
                        # WHERE PREZZO = (SELECT MIN(PREZZO) FROM CAR)
        return cur.fetchall()
    except Error:
        traceback.print_exc()
    finally:
        if con:
            con.close()

if __name__ == "__main__":
        for car in lowestPrice(DB_PATH):
            print(car)