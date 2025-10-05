from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import numpy as np
import requests

from keras.applications import InceptionV3
from keras.applications.inception_v3 import preprocess_input, decode_predictions
from keras.applications import imagenet_utils
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
from io import BytesIO

app = Flask(__name__)
api = Api(app)

#Load pretrained model
model = InceptionV3(weights='imagenet')

#Initialize MongoDB Client
client = MongoClient("mongodb://db:27017")
db = client.ImageClassification
users = db["Users"]
images = db["Images"]

def UserExist(username):
    if users.count_documents({"Username":username}) == 0:
        return False
    else:
        return True
def verifyPw(username, password):
    if not UserExist(username):
        return False

    user = users.find_one({"Username": username})
    if not user:
        return False
    hashed_pw = user["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def verify_credentials(username, password):
    if not UserExist(username):
        return generate_return_dictionary(301, "Invalid Username"), True

    correct_pw = verifyPw(username, password)
    if not correct_pw:
        return generate_return_dictionary(302, "Invalid Password"), True  
    
    return None, False
    
def generate_return_dictionary(status, msg):
    retJson = {
        "status": status,
        "msg": msg
    }
    return retJson

   

def countTokens(username):
    user = users.find_one({"Username": username})
    if not user:
        return 0
    return user["Tokens"]

class Register(Resource):
    def post(self):
        #Step 1 is to get posted data by the user
        postedData = request.get_json()

        #Get the data
        username = postedData["username"]
        password = postedData["password"] #"123xyz"

        if UserExist(username):
            retJson = {
                'status':301,
                'msg': 'User already exists'
            }
            return jsonify(retJson)

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store username and pw into the database
        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Tokens":6
        })

        retJson = {
            "status": 200,
            "msg": "You successfully signed up for the API"
        }
        return jsonify(retJson)
class Login(Resource):
    def post(self):
        #Step 1 is to get posted data by the user
        postedData = request.get_json()

        #Get the data
        username = postedData["username"]
        password = postedData["password"] #"123xyz"

        if not UserExist(username):
            retJson = {
                'status':301,
                'msg': 'Invalid Username'
            }
            return jsonify(retJson)

        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                'status':302,
                'msg': 'Invalid Password'
            }
            return jsonify(retJson)

        retJson = {
            'status':200,
            'msg': 'Login successful'
        }
        return jsonify(retJson)
    
class Classify(Resource):
    def post(self):
        #Step 1 get the posted data
        postedData = request.get_json()

        #Step 2 is to read the data
        username = postedData["username"]
        password = postedData["password"]
        url = postedData["url"]

        #Step 3 Verify credentials
        ret_json, error = verify_credentials(username, password)
        if error:
            return jsonify(ret_json)


        #Step 4 verify user has enough tokens
        tokens = countTokens(username)
        if tokens <= 0:
            return jsonify(generate_return_dictionary(303, "You are out of tokens, please refill"))

        #Download the image, preprocess it and prepare it for classification

        if not url:
            return jsonify(generate_return_dictionary(400, "No url Provided"))

        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        #pre process the image
        img = img.resize(299,299)
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        #Make prediction
        prediction = model.predict(img_array)
        
        #Classify the image
        preds = model.predict(img_array)
        results = imagenet_utils.decode_predictions(preds, top=5)

        ret_json = {}
        for pred in preds[0]:
            ret_json[pred[1]] = float(pred[2]* 100)

        
        #Reduce the tokens by 1
        users.update_one({
            "Username":username
        },{
            "$set":{
                "Tokens":tokens-1
            }
        })

        return jsonify(ret_json)

class refill(Resource):
    def post(self):
        #Step 1 get the posted data
        postedData = request.get_json()

        #Step 2 is to read the data
        username = postedData["username"]
        password = postedData["admin_pw"]
        amount = postedData["amount"]

        #Step 3 Verify credentials
        if not UserExist(username):
            return jsonify(generate_return_dictionary(301, "Invalid Username"))

        correct_pw = "abc123"
        if not password == correct_pw:
            return jsonify(generate_return_dictionary(302, "Invalid Admin Password"))

        #Refill the tokens
        tokens = countTokens(username)
        users.update_one({
            "Username":username
        },{
            "$set":{
                "Tokens":amount + tokens
            }
        })

        return jsonify(generate_return_dictionary(200, "Refilled successfully"))
        
        

    

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Classify, '/classify')
api.add_resource(refill, '/refill')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5025)