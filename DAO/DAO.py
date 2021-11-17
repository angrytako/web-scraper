import sqlite3
from sqlite3.dbapi2 import Connection, Error
import traceback
import sys
import os
import requests as req
from datetime import datetime, timedelta
from DAO.CarParams import CarParams
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from models.Car import Car

DB_PATH = os.path.join(os.path.dirname(current) , "cars.db")

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
            CREATION_DATE DATE NOT NULL,
            LAST_CHECKED DATE NOT NULL
        )"""

def setExpired(car:Car,file:str)->bool:
    con = None
    try:
        con = sqlite3.connect(file)
        cur = con.cursor()
        cur.execute(f"""UPDATE CAR
                            SET EXPIRED = 1, LAST_CHECKED = ?
                            WHERE CAR_URL = ? """, [car.lastChecked, car.url])
        return True
    except Error:
        traceback.print_exc()
        return False
    finally:
        if con:
            con.close()    
def deleteFromDb(link:str,file:str):
    con = None
    try:
        con = sqlite3.connect(file)
        cur = con.cursor()
        cur.execute(f"""DELETE FROM CAR WHERE CAR_URL = ? """, [link])
        cur.execute("commit;")
        return True
    except Error:
        traceback.print_exc()
        return False
    finally:
        if con:
            con.close()  
def checkExpiredAndUpdate(cars:list, con:Connection):
    stillUp = []
    countDeleted = 0
    countUpdated = 0
    cur = con.cursor()
    curTime = datetime.now()
    d = timedelta(days = 1)
    oneDayAgo = curTime - d
    for car in cars:
        if datetime.fromisoformat(car.lastChecked) < oneDayAgo and car.expired != True:  
            car.lastChecked = datetime.now().isoformat()
            if req.head(car.url).status_code>300: 
                cur.execute(f"""UPDATE CAR
                            SET EXPIRED = 1, LAST_CHECKED = ?
                            WHERE CAR_URL = ? """, [car.lastChecked,car.url])
                countDeleted += 1
            else:
                cur.execute(f"""UPDATE CAR
                            SET LAST_CHECKED = ?
                            WHERE CAR_URL = ? """, [car.lastChecked,car.url])
                countUpdated += 1
                stillUp.append(car)

        else: stillUp.append(car)
    if countDeleted > 0 or countUpdated > 0 :
        cur.execute("commit;")
    print(f"EXPIRED:{countDeleted}")
    print(f"CHECKED:{countDeleted + countUpdated}")
    return stillUp



def convertToJson(cars:list)->str:
    if not cars: return None
    if len(cars) == 0: return "[]"
    result = "["
    for car in cars:
        result += car.toJSON() + ","
    i=len(result)-1
    return result[0:i] + "]"

def getAllNonExpiredUrls(file:str)->set:
    con = None
    try:
        con = sqlite3.connect(file)
        cur = con.cursor()
        cur.execute(f"""SELECT CAR_URL FROM CAR WHERE EXPIRED = 0""")
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
        cur.execute(f"""SELECT CAR_URL,NOME,PREZZO,IMG_URL,DATE,EURO,KM,DESCRIPTION,CREATION_DATE,EXPIRED,LAST_CHECKED FROM CAR""")
        cars = []
        for car in cur.fetchall():
            expired = 1
            if car[9] == 1:
                expired = True
            else: expired = False
            cars.append(Car(car[1],car[2],car[0],car[3],car[4],car[5],car[6],car[7],car[8],expired,car[10]))
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
def update(car:Car,file:str)->bool:
    con = None
    try:
        con = sqlite3.connect(file)
        car.updateInDb(con)
        return True
    except Error:
        traceback.print_exc()
        return False
    finally:
        if con:
            con.close()
            
def lowestPrice(file:str):
    con=None
    try:
        con = sqlite3.connect(file)
        cur = con.cursor()
        cur.execute(f"""SELECT CAR_URL,NOME,PREZZO,IMG_URL,DATE,EURO,KM,DESCRIPTION,CREATION_DATE,EXPIRED,LAST_CHECKED FROM CAR 
                        WHERE (PREZZO<4000 OR PREZZO is NULL) and (KM<140000 or KM is NULL) and (EURO>3 OR EURO is NULL) AND EXPIRED=0
                        ORDER BY PREZZO ASC""")
                        # WHERE PREZZO = (SELECT MIN(PREZZO) FROM CAR)
        cars = []
        for car in cur.fetchall():
            expired = 1
            if car[9] == 1:
                expired = True
            else: expired = False
            cars.append(Car(car[1],car[2],car[0],car[3],car[4],car[5],car[6],car[7],car[8],expired, car[10]))
        return convertToJson(checkExpiredAndUpdate(cars,con))
    except Error:
        traceback.print_exc()
    finally:
        if con:
            con.close()
def fromCarParams(file:str,carParams:CarParams)->list:
    con=None
    try:
        con = sqlite3.connect(file)
        cur = con.cursor()
        dbStuff = carParams.toDbStringAndArray()

        cur.execute(dbStuff[0],dbStuff[1])
        cars = []
        for car in cur.fetchall():
            expired = 1
            if car[9] == 1:
                expired = True
            else: expired = False
            cars.append(Car(car[1],car[2],car[0],car[3],car[4],car[5],car[6],car[7],car[8],expired, car[10]))
        return convertToJson(checkExpiredAndUpdate(cars,con))
    except Error:
        traceback.print_exc()
    finally:
        if con:
            con.close()

if __name__ == "__main__":
    # print(numElem(DB_PATH))
    # deleteFromDb("https://www.subito.it/auto/peugeot-206-eco-plus-2010-torino-410665407.htm",DB_PATH)
    # #createTable("cars.db")
    # print(numElem(DB_PATH))
    #print(fromCarParams(DB_PATH, CarParams({"prezzo":{"value":5000, "op":None}})))
    print(fromCarParams(DB_PATH, CarParams({"nome":{"value":"%Opel%", "op":"like"},"prezzo":{"value":6000, "op":None}})))