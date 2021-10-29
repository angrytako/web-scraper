from subito.Subito import SubitoScraper
from autoscout.Autoscout import AutoscoutScraper
from automobile.Automobile import AutomobileScraper
from multiprocessing import Process
from DAO.DAO import createTable, getAllUrls, lowestPrice, numElem
from sqlite3 import Error
import cchardet 

def subito(pageCounter):
    scraper = SubitoScraper(pageCounter)
    scraper.getCars()

def autoscout(pageCounter):
    scraper = AutoscoutScraper(pageCounter)
    scraper.getCars()

def automobile(pageCounter):
    scraper = AutomobileScraper(pageCounter)
    scraper.getCars()

def create_connection(db_file):
    try:
        # print(numElem(db_file))
        # return
        # createTable(db_file)
        # return
        # for car in lowestPrice(db_file):
        #     print(car)
        # return

        proc1 = Process( target=subito,args=(1,) )
        proc2 = Process( target=autoscout,args=(1,) )
        proc3 = Process( target=automobile,args=(1,) )
        proc1.start()
        proc2.start()
        proc3.start()
        proc1.join()
        proc2.join()
        proc3.join()
        quit()
    except Error as e:
        print(e)


if __name__ == '__main__':
    create_connection(".\pythonsqlite.db")
   