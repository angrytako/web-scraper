from subito.Subito import SubitoScraper
from autoscout.Autoscout import AutoscoutScraper
from automobile.Automobile import AutomobileScraper
from multiprocessing import Process
from DAO.DAO import DB_PATH
from sqlite3 import Error
import time

def subito(pageCounter):
    scraper = SubitoScraper(pageCounter)
    scraper.getCars()

def autoscout(pageCounter):
    scraper = AutoscoutScraper(pageCounter)
    scraper.getCars()

def automobile(pageCounter):
    scraper = AutomobileScraper(pageCounter)
    scraper.getCars()

def findCarsAndSave(db_file):
    try:
        time.sleep(10)
        while True:
            proc1 = Process( target=subito,args=(1,) )
            proc2 = Process( target=autoscout,args=(1,) )
            proc3 = Process( target=automobile,args=(1,) )
            proc1.start()
            proc2.start()
            proc3.start()
            proc1.join()
            proc2.join()
            proc3.join()
            time.sleep(60*10)
    except Error as e:
        print(e)


if __name__ == '__main__':
    findCarsAndSave(DB_PATH)
   