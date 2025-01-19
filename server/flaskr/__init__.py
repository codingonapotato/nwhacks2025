import os
from flaskr.constants import *
import flaskr.db as db
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.local import LocalProxy
from flaskr.db import *
from flask import Flask

def create_app(test_config=None):
    # load values from .env
    load_dotenv()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # configure connection to MongoDB
    db.mongoClient.append(MongoClient(os.environ[MONGO_URI]))
    
    database = db.mongoClient[0].get_database("passwords")
    passwords = database.get_collection("passwords")
    passwords.insert_one({"bob@netgear.com" : "Yapyapyapyap"})
    print("Yippee I did it")

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app