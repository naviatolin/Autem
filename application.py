from flask import Flask
from flask_pymongo import PyMongo
from flask import request

app = Flask(__name__)
app.config("MONGO_URI") = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route("/")
def home_page():
