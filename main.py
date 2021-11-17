from flask import request, Flask
from DAO.CarParams import CarParams
from flask_mail import Mail,Message
from DAO import DAO
from models.Car import fromDictionary, Car
from CarScraper import CarScraper
import json
import os
from subito.Subito import SubitoScraper
from autoscout.Autoscout import AutoscoutScraper
from automobile.Automobile import AutomobileScraper
from datetime import datetime
from telethon import TelegramClient
import asyncio

def getRightScraper(url:str)->CarScraper:
    if "subito" in url:
        return SubitoScraper()
    if "autoscout" in url:
        return AutoscoutScraper()
    else: return AutomobileScraper()

async def sendToTelegram(message:str):
    api_id = os.getenv("API_ID")
    api_hash =  os.getenv("API_HASH")
    MyPhone = os.getenv("MY_PHONE")
    reciverNr =  os.getenv("RECIVER_NR")
    client =  TelegramClient(os.getenv("TELEGRAM_CLIENT"), api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(MyPhone)        
        await client.sign_in(MyPhone, input('Enter the code: '))
    try:
        await client.send_message(reciverNr, message)
    except Exception as e:
        print(e)
    finally: 
        await client.disconnect()

app = Flask(__name__, static_folder="static", static_url_path="/")

app.config['MAIL_SERVER']= os.getenv("SERVER")
app.config['MAIL_PORT'] = os.getenv("EMAIL_PORT")
app.config['MAIL_USERNAME'] = os.getenv("EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("PW")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
@app.route('/getCars', methods=["POST"])
def serveGetCars():
    carsSearchDict = request.json
    carsJson = DAO.fromCarParams(file=DAO.DB_PATH,carParams=CarParams(carsSearchDict))
    if carsJson: return carsJson
    else: return "[]"

@app.route("/mail", methods=["POST"])
def sendMail():
    msg = Message("New interesting car!",
                  sender=os.getenv("EMAIL"),
                  recipients=[os.getenv("RECIPIENT_EMAIL")])
    msg.body = json.loads(request.json)["message"]
    mail.send(msg)
    asyncio.run(sendToTelegram(msg.body))
    return "sent"

@app.route("/update", methods=["POST"])
def update():
    car = fromDictionary(request.json)
    DAO.update(car, DAO.DB_PATH)
    return car.url

@app.route("/reload", methods=["POST"])
def reload():
    car = fromDictionary(request.json)
    carScraper = getRightScraper(car.url)
    updatedCar = carScraper.getCarFromUrl(car.url)
    del carScraper

    if updatedCar:
        updatedCar.creationDate = datetime.isoformat(car.creationDate)
        DAO.update(updatedCar, DAO.DB_PATH)
    else:
        updatedCar = car
        updatedCar.expired = True
        DAO.setExpired(car, DAO.DB_PATH)
    return updatedCar.toJSON()

@app.route('/', defaults={'path': ''})
@app.route("/<path:path>")
def static_dir(path):
    return app.send_static_file("index.html")
if __name__ =="__main__":
    app.run(debug=True)


