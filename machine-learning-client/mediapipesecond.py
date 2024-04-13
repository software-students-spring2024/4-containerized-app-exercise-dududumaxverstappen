
import mediapipe as mp
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

base_options = python.BaseOptions(model_asset_path='path/to/gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

image = mp.Image.create_from_file('./nayeon.jpeg')
recognition_result = recognizer.recognize(image)

image = mp.Image.create_from_file(image)

    # Recognize gestures in the input image.
recognition_result = recognizer.recognize(image)

# Process the result.
top_gesture = recognition_result.gestures[0][0] # The top recognized gesture
hand_landmarks = recognition_result.hand_landmarks # Detected hand landmarks

print(top_gesture)
print(hand_landmarks)