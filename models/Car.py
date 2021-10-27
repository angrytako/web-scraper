import json
import sqlite3
import re
class Car:
    def __init__(self,nome,prezzo,url,imgUrl,date,euro,km,description):
        if nome:
            self.nome = nome#.replace("\"","").replace("'","")
        else:
            self.nome=None
        self.prezzo = prezzo
        self.url = url
        self.imgUrl = imgUrl
        self.date = date
        if euro and len(re.findall(r"\d",euro))>0:
            self.euro = int(re.findall(r"\d",euro)[0])
        else:
            self.euro = None
        self.km = km
        if description:
            self.description = description#.replace("\"","").replace("'","")
        else:
            self.description=None
    def __str__(self):
        return f"""
        nome: {self.nome}
        prezzo: {self.prezzo}
        url annuncio: {self.url}
        url immagine: {self.imgUrl}
        data: {self.date}
        euro: {self.euro}
        km: {self.km}
        descrizione: {self.description}
        """
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def saveToDb(self,connection):
        cur = connection.cursor()
        args = [self.url,self.nome,self.prezzo,self.imgUrl,self.date,self.euro,self.km,self.description]
        statement = f"""INSERT INTO CAR (CAR_URL,NOME,PREZZO,IMG_URL,DATE,EURO,KM,DESCRIPTION) 
                        VALUES (?,?,?,?,?,?,?,?)"""
        cur.execute(statement,args)
        cur.execute("commit;")
