from flask import Flask, request, jsonify, render_template
import pymongo
from pymongo import MongoClient
import os
import requests


app = Flask(__name__)

app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/coffee_shops')

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("MONGODB_PW")
DB_HOST = os.getenv("DB_HOST")
uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/?retryWrites=true&w=majority&appName=Cluster0&tlsAllowInvalidCertificates=true"
client = pymongo.MongoClient(uri)
db = client.get_database("cafes")


@app.route('/')
def home():
    return render_template('index.html')


# get users location and forward to machine learning model
@app.route('/find_coffee_shops', methods=['POST'])
def find_coffee_shops():
    
    data = request.get_json()
    machine_learning_client_url = 'http://localhost:5000/find_coffee_shops'

    # send data to machine learning model
    response = requests.post(machine_learning_client_url, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify({'error': 'error in finding coffee shops!'}), 500



# show all results
@app.route('/results', methods=['POST'])
def show_results():
    data = request.get_json()
    latitute = data['latitude']
    longitude = data['longitude']
    
    coffee_shops = db.cafes.find({"latitute": latitute, "longitude": longitude})
    
    shop_list = [shop for shop in coffee_shops]
    return render_template('results.html', coffee_shops=shop_list)



# ---------------------------------------------------------------------------- #
#                                     main                                     #
# ---------------------------------------------------------------------------- #

if __name__ == '__main__':
    FLASK_PORT = os.getenv('FLASK_PORT', '8080')
    app.run(port=FLASK_PORT)