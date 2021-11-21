PARSER = 'html.parser'
#to add lxml again in pipenv
from multiprocessing import Semaphore
from sqlite3.dbapi2 import Error
import sqlite3
import atexit
from models.Car import Car
from DAO.DAO import getAllNonExpiredUrls, DB_PATH
import traceback
import requests as req
import os    
from datetime import datetime

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
    def __init__(self,pageCounter = None):
        if not pageCounter:
            return
        if not self.carsUrls:
            self.carsUrls = getAllNonExpiredUrls(DB_PATH)
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
            print(self.pageCounter, mainUrl,"\nDate:"+ datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
            self.pageCounter+=1
            pageCarsUrls = self.getCarsUrls(mainUrl)
            if pageCarsUrls == None:
                    return
            for carUrl in pageCarsUrls:
                carSup = self.getCarFromUrl(carUrl)
                try:
                    pass
                    if carSup.price <= 3200 and carSup.euro and carSup.euro >= 4 and carSup.km and carSup.km <= 135000 and (not "diesel" in carSup.fuel.lower() or (carSup.euro and carSup.euro >= 6)):
                            req.post(os.getenv("SERVER_URL") + os.getenv("EMAIL_PATH"), json=f'{{"message": "{carSup.url}"}}')
                            print("CANDIDATE:", carSup.url)
                    carSup.saveToDb(connection)
                except Error:
                    traceback.print_exc()
                print(carUrl)
