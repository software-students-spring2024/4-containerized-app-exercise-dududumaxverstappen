import mediapipe as mp
import cv2
from pymongo import MongoClient

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

mongo_client = MongoClient('mongodb+srv://bcdy:BPoOlpuLgv3WKJ62@coffeeshops.5kr79yv.mongodb.net/')
db = mongo_client['gestures']
gestureDB = db['emoji']

video = cv2.VideoCapture(0)

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

# Create a image segmenter instance with the live stream mode:

def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    # Displaying gesture recognition results
    if result.gestures:
        for gesture_list in result.gestures:
            for gesture in gesture_list:
                print(emoji(gesture.category_name)) # Removed the curly braces
                #render_template('fallingEMojis.html')
                
                if gesture.category_name!='None':
                    gesturetolandmark = { "top_gesture": gesture.category_name, "score" : gesture.score, "emoji" : emoji(gesture.category_name)}
                    gestureDB.insert_one(gesturetolandmark)


options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

timestamp = 0
with GestureRecognizer.create_from_options(options) as recognizer:
  # The recognizer is initialized. Use it here.
    while video.isOpened(): 
        # Capture frame-by-frame
        ret, frame = video.read()

        if not ret:
            print("Ignoring empty frame")
            break

        timestamp += 1
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        # Send live image data to perform gesture recognition
        # The results are accessible via the `result_callback` provided in
        # the `GestureRecognizerOptions` object.
        # The gesture recognizer must be created with the live stream mode.
        recognizer.recognize_async(mp_image, timestamp)

        if cv2.waitKey(5) & 0xFF == 27:
            break

video.release()
cv2.destroyAllWindows()