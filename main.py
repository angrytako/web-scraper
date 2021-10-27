from subito.Subito import SubitoScraper
from autoscout.Autoscout import AutoscoutScraper
from multiprocessing import Process
import sqlite3
from sqlite3 import Error

def subito(pageCounter):
    scraper = SubitoScraper(pageCounter)
    scraper.getCars()

def autoscout(pageCounter):
    scraper = AutoscoutScraper(pageCounter)
    scraper.getCars()
CAR_TABLE = f"""CREATE TABLE CAR (
            CAR_URL VARCHAR(40) PRIMARY KEY,
            NOME VARCHAR(40) NOT NULL,
            PREZZO INTEGER NOT NULL,
            IMG_URL VARCHAR(40),
            DATE VARCHAR(12),
            EURO INTEGER,
            KM INTEGER,
            DESCRIPTION VARCHAR(200)
        )"""
def createTable(file):
    con = sqlite3.connect(file)
    cur = con.cursor()
    cur.execute(CAR_TABLE)
    return
def lowestPrice(file):
    con = sqlite3.connect(file)
    cur = con.cursor()
    cur.execute(f"""SELECT NOME,PREZZO,EURO,CAR_URL FROM CAR 
                    WHERE (PREZZO<3000 OR PREZZO is NULL)and (KM<110000 or KM is NULL) and (EURO>3 OR EURO is NULL)""")
                    # WHERE PREZZO = (SELECT MIN(PREZZO) FROM CAR)
    return cur.fetchall()
def create_connection(db_file):
    STOP = [False]
    conn = None
    try:
        # createTable(db_file)
        # return
        # for car in lowestPrice(db_file):
        #     print(car)
        # return

        proc1 = Process( target=subito,args=(1,) )
        proc2 = Process( target=autoscout,args=(1,) )
        proc1.start()
        proc2.start()
        proc1.join()
        proc2.join()
        quit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection(".\pythonsqlite.db")
   