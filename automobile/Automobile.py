import sys
import os
from bs4 import BeautifulSoup
import requests as req
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from CarScraper import PARSER, CarScraper, getDigits
import re
from models.Car import Car


class AutomobileScraper(CarScraper):
    BASE_URL = "https://www.automobile.it"

    def __init__(self,pageCounter = None):
        super().__init__(pageCounter)
        self.imgUrls = None


    def getMainUrl(self)->int:
        if self.pageCounter <= 1:
            return "https://www.automobile.it/torino_comune?classe_emissioni=euro_6,euro_5,euro_4&prezzo_a=max_6000_euro&prezzo_da=1000&radius=300&valutazione_del_venditore=tutti"
        else:
            return f"https://www.automobile.it/torino_comune/page-{self.pageCounter}?classe_emissioni=euro_6,euro_5,euro_4&dove=torino_comune&prezzo_a=max_6000_euro&prezzo_da=1000&radius=100&valutazione_del_venditore=tutti"

    #returns set of all carsUrls, if you haven't seen them before,
    #otherwise assumes that you have reached 'the end' and returns null
    def __getUrlsAndValidate__(self, cars:list)->set:
        doubleNr = 0
        actualCars = 0
        urls=set()
        self.imgUrls = {}
        for car in cars:
            try:
                carUrl = self.BASE_URL + car["href"]
                imgUrl = car.find(class_="Card__ImgContainer").find("img")["data-src"]
            except:
                continue
            actualCars+=1
            if carUrl in self.carsUrls:
                doubleNr +=1
                continue
            self.sem.acquire()
            self.carsUrls.add(carUrl)
            self.sem.release()
            urls.add(carUrl)
            self.imgUrls[carUrl] = imgUrl
        print(f"from {actualCars} to {len(urls)} doubles: {doubleNr}")
        if len(urls)==0:
            return None
        return urls

    def getCarsUrls(self, mainUrl:str)->list:
        mainPage = req.get(mainUrl)
        if mainPage.status_code > 400:
            exit()
        parsedMainPage = BeautifulSoup(mainPage.text,PARSER)
        carsDiv = parsedMainPage.find(class_="Contents")
        carsDivsAndExtras = carsDiv.findAll("a")
        carsUrls = self.__getUrlsAndValidate__(carsDivsAndExtras)
        if carsUrls == None:
            return None
        if len(carsUrls) == 0:
            return None
        return carsUrls

    def getCarFromUrl(self, carUrl:str)->Car:
        carPage = req.get(carUrl)
        if carPage.status_code == 404:
            return None
        parsedCarPage = BeautifulSoup(carPage.text,PARSER)
        infos = parsedCarPage.findAll(class_="Item")
        name = parsedCarPage.find("h1").text
        imgUrl = None
        if self.imgUrls:
            imgUrl = self.imgUrls[carUrl]
        if not imgUrl:
            allImgs = parsedCarPage.findAll("img")
            for img in allImgs:
                try:
                    if img["alt"] in name or name in img["alt"]:
                        print(img["src"])
                        imgUrl = self.BASE_URL+ img["src"]
                        break
                except:
                    pass
        price = int(getDigits(parsedCarPage.find(class_="Price").text))
        date=None
        km = None
        euro = None
        fuel = None
        description = parsedCarPage.find(class_="Description__Container").text
        for info in infos:
            if "Chilometri" in info.text:
                km = getDigits(info.find("div").text)
            elif "Classe emissioni" in info.text:
                euro = getDigits(info.find("div").text)
            elif "Carburante" in info.text:
                fuel = info.find("div").text
        attributes = parsedCarPage.find(class_="Attributes__Container")
        for attr in attributes:
            if attr and attr.text and re.match(r"[a-zA-Z ]*\d\d\d\d",attr.text):
               date = int(getDigits(re.findall(r"\d\d\d\d",attr.text)))
        if fuel and "gas di petrolio liquefatto" in fuel.lower():
            fuel = "GPL"
        return Car(name,price,carUrl,imgUrl,date,euro,km,description,fuel)

if __name__ == "__main__":
    scraper = AutomobileScraper(1)
    scraper.getCars()