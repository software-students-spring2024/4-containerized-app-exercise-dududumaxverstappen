import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import base64
import numpy as np
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)


try:
    uri = "mongodb://mongodb:27017/"
    client = MongoClient(uri)
    client.admin.command("ping")
    db = client["gestures"]
    print("Connected!")

except Exception as e:
    print(e)


base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)


def emoji(hand):
    if hand == 'Closed_Fist':
        return "\u270A"
        #print("\u270A")  
    elif hand == 'Open_Palm':
        return "\u270B"
        #print("\u270B")  
    elif hand == 'Pointing_Up':
        return "\U0001F446"
        #print("\U0001F446")  
    elif hand == 'Thumb_Down':
        return "\U0001F44E"
        #print("\U0001F44E")  
    elif hand == 'Thumb_Up':
        return "\U0001F44D"
        #print("\U0001F44D")  
    elif hand == 'Victory':
        return "\u270C"
        #print("\u270C")  
    elif hand == 'ILoveYou':
        return "\U0001F91F"
        #print("\U0001F91F")
    # if no gesture detected then return question mark emoji
    else:
        return "\U00002753"


@app.route('/server_endpoint', methods=['POST'])
def handle_image():
    data = request.json['image']
    # Decode the data URL
    header, encoded = data.split(",", 1)
    data = base64.b64decode(encoded)
    # Convert to a numpy array
    nparr = np.frombuffer(data, np.uint8)
    # Decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # Now you can save this image and use create_from_file or process directly
    cv2.imwrite('captured_image.png', img)
    # Assuming create_from_file() is now appropriate
    processed_image = gesture('captured_image.png')
    return "Image processed"


@app.route('/gesture', methods=['POST'])
def gesture(captured_image):
    image = mp.Image.create_from_file('captured_image')
    recognition_result = recognizer.recognize(image)

    # Process the result.
    top_gesture = recognition_result.gestures[0][0] # The top recognized gesture
    hand_landmarks = recognition_result.hand_landmarks # Detected hand landmarks
    ges_emoji = emoji(top_gesture)

    # insert the gesture to the database
    gesturetolandmark = { "result": { "top_gesture": top_gesture, "emoji" : ges_emoji }}
    db.insert_one(gesturetolandmark)


