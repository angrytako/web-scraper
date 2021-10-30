PARSER = 'lxml'
from multiprocessing import Semaphore
from sqlite3.dbapi2 import Error
import sqlite3
import atexit
from models.Car import Car
from DAO.DAO import getAllUrls,DB_PATH
import traceback

def terminationHandler(connection):
    connection.close()
    print(__name__,"CLOSED CONNECTION")

def getDigits(str:str)->str:
    res = ""
    for let in list(str):
        if let.isdigit():
            res += let
    return res

class CarScraper:
    carsUrls = None
    sem = None
    def __init__(self,pageCounter):
        if not self.carsUrls:
            self.carsUrls = getAllUrls(DB_PATH)
        if not self.sem:
            self.sem = Semaphore(1)
        self.pageCounter=pageCounter

    def getCarsUrls(self, mainUrl:str)->list:
        pass
    def getCarFromUrl(self, carUrl:str)->Car:
        pass
    def __getUrlsAndValidate__(self, cars:list)->set:
        pass
    def getMainUrl(self, pageCounter:int)->int:
        pass

    def getCars(self):
        connection = sqlite3.connect(DB_PATH)
        atexit.register(terminationHandler, connection)
        while(True):
            mainUrl = self.getMainUrl()
            print(self.pageCounter, mainUrl)
            self.pageCounter+=1
            pageCarsUrls = self.getCarsUrls(mainUrl)
            if pageCarsUrls == None:
                    return
            for carUrl in pageCarsUrls:
                carSup = self.getCarFromUrl(carUrl)
                try:
                    pass
                    if carSup.price <=3000 and carSup.euro and carSup.euro >= 4:
                        print("CANDIDATE:")
                    carSup.saveToDb(connection)
                except Error:
                    traceback.print_exc()
                print(carUrl)