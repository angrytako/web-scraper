import json
import re
from sqlite3.dbapi2 import Connection
from datetime import datetime

class Car:
    def __init__(self,name,price,url,imgUrl,date,euro,km,description, fuel,
                 creationDate = None, expired = False, lastChecked = None):
        if name:
            self.name = name
        else:
            self.name=None
        self.price = int(price)
        self.url = url
        self.imgUrl = imgUrl
        self.date = date
        if euro and isinstance(euro,str) and len(re.findall(r"\d",euro))>0:
            self.euro = int(re.findall(r"\d",euro)[0])
        elif euro and isinstance(euro,int):
            self.euro = euro
        else:
            self.euro = None
        if km: 
            self.km = int(km)
        else:
            self.km=None
        if description:
            self.description = description
        else:
            self.description=None
        if fuel:
            self.fuel = fuel
        else:
            self.fuel=None
        self.creationDate = creationDate if creationDate else datetime.now().isoformat()
        self.lastChecked = lastChecked if lastChecked else datetime.now().isoformat()
        self.expired = expired

    def __str__(self):
        return f"""
        name: {self.name}
        prezzo: {self.price}
        url annuncio: {self.url}
        url immagine: {self.imgUrl}
        data: {self.date}
        euro: {self.euro}
        km: {self.km}
        aggiunto il: {self.creationDate}
        link scaduto: {self.expired}
        last checked: {self.lastChecked}
        descrizione: {self.description}
        carburante: {self.fuel}
        """
    def toArray(self):
        return [self.url,self.name,self.price,self.imgUrl,self.date,self.euro,self.km,
                self.description,self.fuel,self.creationDate, self.expired,self.lastChecked]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def saveToDb(self, connection:Connection):
        cur = connection.cursor()
        args = self.toArray()
        statement = f"""INSERT INTO CAR (CAR_URL,NOME,PREZZO,IMG_URL,DATE,EURO,KM,DESCRIPTION,FUEL,CREATION_DATE,EXPIRED,LAST_CHECKED) 
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
        cur.execute(statement,args)
        cur.execute("commit;")       

    def updateInDb(self,connection:Connection):
        cur = connection.cursor()
        args = [self.name,self.price,self.imgUrl,self.date,self.euro,self.km,
                self.description,self.fuel,self.expired,self.lastChecked,self.url]
        statement = f"""UPDATE CAR 
                        SET NOME = ?, PREZZO = ?, IMG_URL = ?, DATE = ?, EURO = ?,
                        KM = ?, DESCRIPTION = ?,FUEL = ?, EXPIRED = ?, LAST_CHECKED = ? 
                        WHERE CAR_URL = ?"""
        cur.execute(statement,args)
        cur.execute("commit;")      


def fromDictionary(carDict:dict) ->Car:
    return Car(name=carDict["name"],price=int(carDict["price"]),url=carDict["url"],
                imgUrl=carDict["imgUrl"],date = int(carDict["date"]) ,euro = int(carDict["euro"]) if carDict["euro"]  else None,
                km = int(carDict["km"]), description = carDict["description"], fuel =carDict["fuel"],
                creationDate=datetime.fromisoformat(carDict["creationDate"]),
                expired=carDict["expired"],lastChecked=datetime.fromisoformat(carDict["lastChecked"]))