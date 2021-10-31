from flask import Flask, jsonify,send_from_directory
from DAO import DAO
app = Flask(__name__, static_folder="static", static_url_path="/")


@app.route('/lowest')
def serveLowest():
    return DAO.lowestPrice("car.db")
@app.route('/', defaults={'path': ''})
@app.route("/<path:path>")
def static_dir(path):
    return app.send_static_file("index.html")
if __name__ =="__main__":
    app.run(debug=True)


