import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from bs4 import BeautifulSoup
import requests as req
from CarScraper import PARSER, CarScraper,getDigits
from models.Car import Car
import re

class AutoscoutScraper(CarScraper):
    BASE_URL = "https://www.autoscout24.it"

    #returns set of all carsUrls, if you haven't seen them before,
    #otherwise assumes that you have reached 'the end' and returns null
    def __getUrlsAndValidate__(self, cars:list)->set:
        doubleNr = 0
        actualCars = 0
        urls=set()
        for car in cars:
            carAncor = car.find("a")
            if carAncor == None:
                continue
            carUrl =self.BASE_URL+ carAncor["href"]
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

    def getCarsUrls(self, mainUrl:str)->list:
        mainPage = req.get(mainUrl)
        parsedMainPage = BeautifulSoup(mainPage.text,PARSER)
        cars = parsedMainPage.select(".cl-list-element.cl-list-element-gap")
        pageCarsUrls = self.__getUrlsAndValidate__(cars)
        if pageCarsUrls == None:
            return None
        if len(pageCarsUrls) == 0:
            return None
        return pageCarsUrls

    def getMainUrl(self)->int:
        return f"https://www.autoscout24.it/lst/?sort=standard&desc=0&ustate=N%2CU&page={self.pageCounter}&lon=7.68307&lat=45.06838&zip=Torino&zipr=300&cy=I&atype=C&fc=3&qry=GPL&recommended_sorting_based_id=9b87ca24-1422-4cda-8286-a94877ffa607&"

    def getCarFromUrl(self, carUrl:str)->Car:
        carPage = req.get(carUrl)
        if carPage.status_code == 404:
            return None
        parsedCarPage = BeautifulSoup(carPage.text,PARSER)
        kmText = parsedCarPage.find(class_="cldt-stage-basic-data").find("span").text
        try:
            km = int(kmText.split(" ")[0].replace(".",""))
        except:
            km=None
        carName = parsedCarPage.find("h1").text.replace("\n"," ")
        price = int(getDigits(parsedCarPage.find(class_="cldt-price").find("h2").text.replace(".","")))
        try:
            imgUrl = parsedCarPage.find(class_="as24-carousel__item").find("img")["src"]
        except:
            imgUrl=None
        euro=None
        fuel=None
        date=None
        description=None
        descriptionElem = parsedCarPage.find_all(attrs={"data-type":"description"})
        if len(descriptionElem) >= 1: 
            description= descriptionElem[0].text.replace("\n","")
        dataClusters = parsedCarPage.find_all("dl")
        for dataCluster in dataClusters:
            for i,dataTag in enumerate(dataCluster.find_all(["dd","dt"])):
                if "Classe emissioni" in dataTag.text and i<len(dataCluster)-1:
                    euro =  dataTag.findNext().text.replace("\n","")
                elif "Alimentazione" in dataTag.text and i<len(dataCluster)-1:
                    fuel = dataTag.findNext().text.replace("\n","")
                elif "Anno" in dataTag.text and i<len(dataCluster)-1:
                    try:
                        date = int(dataTag.findNext().text)
                    except:
                        pass
        if euro == None or re.match(r"Euro\s?\d",euro)==None:
                        euro = re.search(r"Euro\s?\d",parsedCarPage.text)
                        if euro != None:
                            euro = euro.group(0)
        if fuel and "gas di petrolio liquefatto" in fuel.lower():
            fuel = "GPL"
        return Car(carName,price,carUrl,imgUrl,date,euro,km,description,fuel)


if __name__ == "__main__":
    scraper = AutoscoutScraper(1)
    scraper.getCars()