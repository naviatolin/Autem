""" Initiliaze Flask app."""
from flask import Flask
from config import Config
from flask_login import LoginManager
from bson.objectid import ObjectId
import os
from flask_pymongo import PyMongo
import json
import datetime
from bson.objectid import ObjectId #

class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)
app.config.from_object(Config)
mongo=PyMongo(app)
db = mongo.db
col = mongo.db[]

app.json_encoder = JSONEncoder

login = LoginManager(app)

from app import routes