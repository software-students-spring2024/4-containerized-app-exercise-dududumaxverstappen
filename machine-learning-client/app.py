from flask import Flask, request, jsonify
import requests
from pymongo import MongoClient

app = Flask(__name__)

# set up mongo 
mongo_client = MongoClient('mongodb+srv://bcdy:n7ZL4YrKcJac2SeT@cafes.cm5pzwe.mongodb.net/?retryWrites=true&w=majority&appName=cafes')
db = mongo_client['cafes']  # db name
cafesCollection = db['cafes']  # collection name

@app.route('/find_cafes', methods=['POST'])
def find_cafes():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']

    google_api_key = 'AIzaSyBPekmNdy7JNyy9ngxDyEOKpy1RIKeirWs'  # Replace with your actual Google API Key
    places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=1000&type=cafe&key={google_api_key}"
    response = requests.get(places_url)
    results = response.json().get('results', [])

    # cafe data -> mongo db
    # pull stats from json
    # insert into collection 
    for cafe in results:
        cafe_data = {
            "name": cafe.get("name"),
            "location": cafe["geometry"]["location"],
            "vicinity": cafe.get("vicinity"),
            "rating": cafe.get("rating"),
            "user_ratings_total": cafe.get("user_ratings_total")
        }
        cafesCollection.insert_one(cafe_data)

    # basic info - name and location of cafe
    simplified_results = [
        {"name": cafe.get("name"), "address": cafe.get("vicinity")} for cafe in results
    ]

    return jsonify(simplified_results)

if __name__ == '__main__':
    app.run(debug=True, port=5001)