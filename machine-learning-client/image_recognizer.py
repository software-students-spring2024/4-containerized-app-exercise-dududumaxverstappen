import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

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
    
# STEP 2: Create an GestureRecognizer object.
base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)


# STEP 3: Load the input image.
image = mp.Image.create_from_file('./nayeon.jpeg')

# STEP 4: Recognize gestures in the input image.
recognition_result = recognizer.recognize(image)

# STEP 5: Process the result. In this case, visualize it.

top_gesture = recognition_result.gestures[0][0]
hand_landmarks = recognition_result.hand_landmarks


print(emoji(top_gesture.category_name))