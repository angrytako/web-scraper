import json
import re
from sqlite3.dbapi2 import Connection
from datetime import datetime

class Car:
    def __init__(self,name,price,url,imgUrl,date,euro,km,description, 
                 creationDate = datetime.now().isoformat(), expired = False, lastChecked = datetime.now().isoformat()):
        if name:
            self.name = name
        else:
            self.name=None
        self.price = price
        self.url = url
        self.imgUrl = imgUrl
        self.date = date
        if euro and isinstance(euro,str) and len(re.findall(r"\d",euro))>0:
            self.euro = int(re.findall(r"\d",euro)[0])
        elif euro and isinstance(euro,int):
            self.euro = euro
        else:
            self.euro = None
        self.km = km
        if description:
            self.description = description
        else:
            self.description=None
        self.creationDate = creationDate
        self.expired = expired
        self.lastChecked = lastChecked

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
        """
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def saveToDb(self,connection:Connection):
        cur = connection.cursor()
        args = [self.url,self.name,self.price,self.imgUrl,self.date,self.euro,self.km,
                self.description,self.creationDate, self.expired,self.lastChecked]
        statement = f"""INSERT INTO CAR (CAR_URL,NOME,PREZZO,IMG_URL,DATE,EURO,KM,DESCRIPTION,CREATION_DATE,EXPIRED,LAST_CHECKED) 
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
        cur.execute(statement,args)
        cur.execute("commit;")
