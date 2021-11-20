

class CarParams:
    paramsNames = ["nome","prezzo","url","imgUrl","date","euro","km","description","fuel","creationDate","expired","lastChecked"]
    paramsDefault = { "nome": {"value": None, "op":None },"prezzo": {"value":4000,"op":"<=" },
                    "url": {"value": None, "op":None }, "imgUrl": {"value": None, "op": None },
                    "date": {"value": None, "op":None },"euro": {"value":4,"op":">=" },"km": {"value":130000,"op":"<="},
                    "description": {"value": None, "op":None },"fuel": {"value": None, "op":None } ,"creationDate": {"value": None, "op": None },
                    "expired": {"value":False,"op":"="},"lastChecked": {"value": None, "op":None } }
    def __init__(self, carDict):
       for paramName in self.paramsNames:
            try:
                self.__setattr__(paramName,{"value":carDict[paramName]["value"]})
                try:
                    if carDict[paramName]["op"]:
                        self.__getattribute__(paramName)["op"] = carDict[paramName]["op"]
                    else:
                        self.__getattribute__(paramName)["op"] = self.paramsDefault[paramName]["op"]

                except:
                    self.__getattribute__(paramName)["op"] = self.paramsDefault[paramName]["op"]
            except:
                self.__setattr__(paramName,{"value":self.paramsDefault[paramName]["value"]})
                self.__getattribute__(paramName)["op"] = self.paramsDefault[paramName]["op"]


    def __str__(self):
        return f"""
        name: {self.nome["value"]}
        prezzo: {self.prezzo["value"]}
        url annuncio: {self.url["value"]}
        url immagine: {self.imgUrl["value"]}
        data: {self.date["value"]}
        euro: {self.euro["value"]}
        km: {self.km["value"]}
        aggiunto il: {self.creationDate["value"]}
        link scaduto: {self.expired["value"]}
        last checked: {self.lastChecked["value"]}
        descrizione: {self.description["value"]}
        fuel: {self.fuel["value"]}
        """
    def toDbStringAndArray(self):
        validParamsCounter = 0
        dbString = "SELECT CAR_URL,NOME,PREZZO,IMG_URL,DATE,EURO,KM,DESCRIPTION,FUEL,CREATION_DATE,EXPIRED,LAST_CHECKED FROM CAR WHERE"
        dbStringArgs = []
        for paramName in self.paramsNames:
            param = self.__getattribute__(paramName)
            paramValue = param["value"]
            if(paramValue != None):
                validParamsCounter += 1
                dbString = dbString + f" ({paramName} {param['op']} ? OR {paramName} is NULL) and"
                dbStringArgs.append(param['value'])
        if(validParamsCounter == 0):
            return ("SELECT * FROM CAR",[])
        else:
            dbString = dbString[:-3]
        print(dbString,dbStringArgs)
        return (dbString, dbStringArgs)
if __name__ == "__main__":
    testParams = CarParams({"prezzo":{"value":5000, "op":None}})
    testParams = CarParams({})
    #testParams = CarParams({"prezzo":{"value":None, "op":None},"euro":{"value":None, "op":None}, "km":{"value":None, "op":None}, "expired":{"value":None, "op":None}})
    print(testParams)
    dbStuff = testParams.toDbStringAndArray()

