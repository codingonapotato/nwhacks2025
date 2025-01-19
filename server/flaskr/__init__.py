import base64
import os
from flaskr.constants import *
import flaskr.db as db
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.db import *
from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

def create_app(test_config=None):
    # load values from .env
    load_dotenv()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # configure connection to MongoDB
    # this is on EC2
    # client = MongoClient(
    #     os.environ[MONGO_URI],
    #     ssl=True,
    #     tlsCAFile="C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\certifi\\cacert.pem"
    # )


    # this locally
    client = MongoClient(
    os.environ[MONGO_URI]
    )

    db.mongoClient.append(client)
    database = db.mongoClient[0].get_database("passwords")
    passwordsDB = database.get_collection("passwords")

    # setup public key (configure only once)
    if not os.path.exists("private_key.pem"):
        private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size = 2048
        )
        serialized_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
            )

        # Save the serialized public key to a .pem file
        try:
            with open("private_key.pem", "wb") as pem_file:
                pem_file.write(serialized_private_key)
            print(f"Private key saved to private_key.pem")
        except Exception as e:
            print(e)
    else:
        print(f"Private key file already exists.")

    try:
        with open('private_key.pem', "rb") as f:    # read in binary 
            private_key = f.read()
            private_key = serialization.load_pem_private_key(private_key, password=None)
            public_key = private_key.public_key()
            serialized_public_key = public_key.public_bytes(
            encoding = serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()

    except Exception as e:
        print(e)

    @app.route('/')
    def default():
        message = {'message': 'hello'}
        return jsonify(message)
    # api endpoints
    @app.route('/register', methods=['POST'])
    def registerUser():
        data = request.get_json()
        email, password = data["email"], data["password"] # TODO: Decrypt with private key
        response = {
            "message" : {"email" : email, "password" : password, "public_key" : serialized_public_key}, 
            "status" : 404
        }
        print(email)
        print(password)
        dbResponse = passwordsDB.insert_one({"email" : email, "password": generate_password_hash(password)})
        if dbResponse.inserted_id:
            response["status"] = 200
        return jsonify(response)

    @app.route('/check-user', methods=['POST'])
    def checkUser():
        data = request.get_json()
        response = {
            "message" : data["email"], 
            "status" : 404
        }
        print(data["email"])
        dbResponse = passwordsDB.find({"email" : data["email"]})
        result = next(dbResponse, None)

        if result:
            response["status"] = 200

        # print(dbResponse)
        # if len(list(dbResponse)):
        #     response["status"] = 200
           
        return jsonify(response)

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        data = request.get_json()

        email, password = data["email"], data["password"] # TODO: Decrypt with private key
        print(password)
        encrypted_password_bytes = base64.b64decode(password)
        response = {
            "message" : {"email" : email, "password" : password}, 
            "status" : 404
        }
        print(encrypted_password_bytes)
        dbResponse = passwordsDB.find({"email" : data["email"]})
        result = next(dbResponse, None)

        if not result:
            print("not found")
            return jsonify(response)

        dbPassword = result["password"]
        print(dbPassword)

        # decrypt the password using private key
        try:
            decrypted_password = private_key.decrypt(
                encrypted_password_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            ).decode()
            print(decrypted_password)
            if check_password_hash(dbPassword,decrypted_password):
                response["status"] = 200
        except Exception as e:
            print(e)
            return jsonify(response)
        
        return jsonify(response)       

    return app