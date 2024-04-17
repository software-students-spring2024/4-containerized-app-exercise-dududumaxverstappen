from flask import Flask, render_template, Response
from pymongo import MongoClient
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

try:
    DB_USER = os.getenv("MONGODB_USER")
    DB_PASSWORD = os.getenv("MONGO_PWD")
    DB_HOST = os.getenv("DB_HOST")
    uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@c{DB_HOST}.5kr79yv.mongodb.net/"
    mongo_client = MongoClient(uri)
    db = mongo_client["gestures"]
    gestureDB = db["emoji"]
except Exception as e:
    print(e)


def emoji(hand):
    if hand == "No gesture detected":
        # if no hand detected
        return "\U0001FAE5"
    if hand == "Closed_Fist":
        return "\u270A"
    elif hand == "Open_Palm":
        return "\u270B"
    elif hand == "Pointing_Up":
        return "\U0001F446"
    elif hand == "Thumb_Down":
        return "\U0001F44E"
    elif hand == "Thumb_Up":
        return "\U0001F44D"
    elif hand == "Victory":
        return "\u270C"
    elif hand == "ILoveYou":
        return "\U0001F91F"
    else:
        # hand detected bit not recognized
        return "\U00002753"


# show home page
@app.route("/")
def index():
    return render_template("index.html")


# get last emoji from database
@app.route("/get_emoji", methods=["GET"])
def get_emoji():
    # Retrieve latest emoji from MongoDB
    latest_gesture = gestureDB.find_one({}, sort=[("timestamp", -1)])
    top_gesture = latest_gesture["result"]["top_gesture"]
    emoji_data = emoji(top_gesture)

    return Response(emoji_data, mimetype="text/plain")


# show results, get data from database
@app.route("/results")
def results():
    return render_template("fallingEmojis.html")


# ---------------------------------------------------------------------------- #
#                                     main                                     #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
