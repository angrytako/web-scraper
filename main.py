from flask import Flask, request
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

def getRightScraper(url:str)->CarScraper:
    if "subito" in url:
        return SubitoScraper()
    if "autoscout" in url:
        return AutoscoutScraper()
    else: return AutomobileScraper()
app = Flask(__name__, static_folder="static", static_url_path="/")

app.config['MAIL_SERVER']= os.getenv("SERVER")
app.config['MAIL_PORT'] = os.getenv("EMAIL_PORT")
app.config['MAIL_USERNAME'] = os.getenv("EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("PW")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
@app.route('/lowest')
def serveLowest():
    carsJson = DAO.lowestPrice(DAO.DB_PATH)
    if carsJson: return carsJson
    else: return "[]"

@app.route("/mail", methods=["POST"])
def sendMail():
    msg = Message("New interesting car!",
                  sender=os.getenv("EMAIL"),
                  recipients=[os.getenv("RECIPIENT_EMAIL")])
    msg.body = json.loads(request.json)["message"]
    mail.send(msg)
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


