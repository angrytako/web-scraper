PATH = "./chromedriver.exe"
PARSER = 'lxml'
from sqlite3.dbapi2 import Error
import sqlite3
import atexit
from models.Car import Car

def terminationHandler(connection):
    connection.close()
    print("CLOSED CONNECTION")

def getDigits(str:str)->str:
    res = ""
    for let in list(str):
        if let.isdigit():
            res += let
    return res

class CarScraper:
    def __init__(self,pageCounter):
        self.carsUrls = set()
        self.cars = []
        self.pageCounter=pageCounter
    def getCarsUrls(self, mainUrl:str)->list:
        pass
    def getCarFromUrl(self, carUrl:str)->Car:
        pass
    def __getUrlsAndValidate__(self, cars:list)->set:
        pass
    def getMainUrl(self, pageCounter:int)->int:
        pass
    def scrape():
        pass
    def getDataLikeModel():
        pass

    def getCars(self):
        connection = sqlite3.connect(".\pythonsqlite.db")
        atexit.register(terminationHandler,connection)
        while(True):
            mainUrl = self.getMainUrl()
            print(self.pageCounter, mainUrl)
            self.pageCounter+=1
            pageCarsUrls = self.getCarsUrls(mainUrl)
            if pageCarsUrls == None:
                    #terminationHandler(connection)
                    return
            for carUrl in pageCarsUrls:
                carSup = self.getCarFromUrl(carUrl)
                try:
                    pass
                    #carSup.saveToDb(connection)
                except Error:
                    print(Error)
                print(carUrl)