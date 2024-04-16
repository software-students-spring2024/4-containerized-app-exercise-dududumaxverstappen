from flask import Flask, request, jsonify, render_template, Response
from pymongo import MongoClient
from PIL import Image
import os
import requests
#from dotenv import load_dotenv
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

CORS(app)



try:
    uri = "mongodb://mongodb:27017/"
    client = MongoClient(uri)
    #client.admin.command("ping")
    db = client["gestures"]
    gestureDB = db["emoji"]
    print("Connected!")

except Exception as e:
    print(e)


def emoji(hand):
    if hand == 'Closed_Fist':
        return "\u270A"
    elif hand == 'Open_Palm':
        return "\u270B"
    elif hand == 'Pointing_Up':
        return "\U0001F446"
    elif hand == 'Thumb_Down':
        return "\U0001F44E"
    elif hand == 'Thumb_Up':
        return "\U0001F44D" 
    elif hand == 'Victory':
        return "\u270C"
    elif hand == 'ILoveYou':
        return "\U0001F91F"


# show home page
@app.route('/')
def index():
    return render_template('index.html')


"""# upload pic
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['picture']
    picture = Image.open(file)"""
    
    


# get last emoji from database
@app.route('/get_emoji', methods=['GET'])
def get_emoji():
    # Retrieve latest emoji from MongoDB
    latest_gesture = gestureDB.find_one(
        {},
        sort=[('timestamp', -1)]
    )
    top_gesture = latest_gesture['result']['top_gesture']
    emoji_data = emoji(top_gesture)
    
    return Response(emoji_data, mimetype='text/plain')


# show results, get data from database
@app.route('/results')
def results():
    return render_template('fallingEmojis.html')


# ---------------------------------------------------------------------------- #
#                                     main                                     #
# ---------------------------------------------------------------------------- #

if __name__ == '__main__':
    app.run(debug=True, port=5001)