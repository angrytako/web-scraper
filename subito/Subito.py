from sqlite3.dbapi2 import Error
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import requests as req
import sys
import os
import re

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from models.Car import Car
from CarScraper import PARSER, CarScraper


def terminationHandler(connection):
    connection.close()
    print("CLOSED CONNECTION")


class SubitoScraper(CarScraper):

    def getCarsUrls(self, mainUrl:str)->list:
        mainPage = req.get(mainUrl)
        paresedMainPage = BeautifulSoup(mainPage.text,PARSER)
        carsDiv = paresedMainPage.find(class_="items")
        cars = carsDiv.findAll(class_="items__item")
        pageCarsUrls = self.__getUrlsAndValidate__(cars)
        if pageCarsUrls == None:
            return None
        if len(pageCarsUrls) == 0:
            return None
        return pageCarsUrls

    #carsUrls gets changed by func. Gets added new urls
    def getCarFromUrl(self, carUrl:str)->Car:
        carPage = req.get(carUrl)
        if carPage.status_code == 404:
            return None
        parsedCarPage = BeautifulSoup(carPage.text,PARSER)
        carName = parsedCarPage.find("h1").text
        priceContainer = parsedCarPage.find(id="sticky-cta-container")
        priceElem = priceContainer.find("span")
        price = ""
        for s in list(priceElem.text):
            if s.isdigit():
                price = price + s
        price = int(price)

        #TODO trovare un modo per prendere tutte le immagini, se possibile senza js
        imageContainer = parsedCarPage.find("figure")
        images = imageContainer.find("img")
        imgUrl = images["src"]

        description = None
        for h2 in parsedCarPage.findAll("h2"):
            if "Descrizione" in h2.text:
                section = h2.parent
                description = section.find("p").text

        mainData = parsedCarPage.find(class_="main-data")
        mainDataContainer = mainData.find("div")
        allMains = mainDataContainer.findAll("div")
        date = None
        euro = None
        km = None
        for quadrant in allMains:
            if "/" in quadrant.text and quadrant.text.split("/")[0].isdecimal():
                date=quadrant.text.split("/")[1]
            elif "Euro" in quadrant.text:
                euro = quadrant.text
            elif "Km" in quadrant.text and quadrant.text.split(" ")[0].isdecimal():
                km = int(quadrant.text.split(" ")[0])
        if euro == None:
            euro = re.search(r"Euro\s?\d",parsedCarPage.text)
            if euro != None:
                euro = euro.group(0)
        return Car(carName,price,carUrl,imgUrl,date,euro,km,description)

#returns set of all carsUrls, if you haven't seen them before,
#otherwise assumes that you have reached 'the end' and returns null
    def __getUrlsAndValidate__(self, cars:list)->set:
        tollerance = len(cars)
        doubleNr = 0
        actualCars = 0
        urls=set()
        for car in cars:
            carAncor = car.find("a")
            if carAncor == None:
                continue
            carUrl = carAncor["href"]
            actualCars+=1
            if carUrl in self.carsUrls:
                doubleNr +=1
                continue
            self.sem.acquire()
            self.carsUrls.add(carUrl)
            self.sem.release()
            urls.add(carUrl)        
        print(f"from {actualCars} to {len(urls)} doubles: {doubleNr}")
        if len(urls)==0:
            return None
        return urls

    def getMainUrl(self)->int:
        return f"https://www.subito.it/annunci-piemonte/vendita/auto/?o={self.pageCounter}&cvs=1&ps=1000&me=21&fu=3"


if __name__ == "__main__":
    scraper = SubitoScraper(1)
    scraper.getCars()