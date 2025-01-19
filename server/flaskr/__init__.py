import os
from flaskr.constants import *
import flaskr.db as db
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from flaskr.db import *
from flask import Flask, request, jsonify

def create_app(test_config=None):
    # load values from .env
    load_dotenv()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # configure connection to MongoDB
    db.mongoClient.append(MongoClient(os.environ[MONGO_URI]))
    
    database = db.mongoClient[0].get_database("passwords")
    passwordsDB = database.get_collection("passwords")

    # api endpoints
    @app.route('/register', methods=['POST'])
    def registerUser():
        data = request.get_json()

    @app.route('/check-user', methods=['POST'])
    def checkUser():
        response = {
            "message" : data["email"], 
            "status" : 404
        }
        data = request.get_json()
        email = passwordsDB.find(data["email"]).toArray()
        if email:
            response["status"] = 200
        return jsonify(response)

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
    return app