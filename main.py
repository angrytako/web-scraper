from flask import Flask, request
from flask_mail import Mail,Message
from DAO import DAO
import json
import os
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
    car = request.json
    print(car["price"])
    return car["url"]


@app.route('/', defaults={'path': ''})
@app.route("/<path:path>")
def static_dir(path):
    return app.send_static_file("index.html")
if __name__ =="__main__":
    app.run(debug=True)


