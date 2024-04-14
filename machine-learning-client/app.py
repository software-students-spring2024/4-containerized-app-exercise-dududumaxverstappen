from matplotlib import pyplot as plt
import mediapipe as mp
#from mediapipe.framework.formats import landmark_pb2
import cv2
import math
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
#input images
import cv2
import mediapipe as mp



plt.rcParams.update({
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.spines.left': False,
    'axes.spines.bottom': False,
    'xtick.labelbottom': False,
    'xtick.bottom': False,
    'ytick.labelleft': False,
    'ytick.left': False,
    'xtick.labeltop': False,
    'xtick.top': False,
    'ytick.labelright': False,
    'ytick.right': False
})

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

#Setup input from camera
cap=cv2.VideoCapture(0)
hands=mp_hands.Hands()

#DEFINING FUNCTIONS 
#Match gesture with emoji
def emoji(category_name):
    gesture_emojis = {
        'Closed_Fist': '\u270A',
        'Open_Palm': '\u270B',
        'Pointing_Up': '\U0001F446',
        'Thumb_Down': '\U0001F44E',
        'Thumb_Up': '\U0001F44D',
        'Victory': '\u270C',
        'ILoveYou': '\U0001FAF6'
    }
"""def emoji(hand):
    if hand == 'Closed_Fist':
        print('\u270A')  
    elif hand == 'Open_Palm':
        print('\u270B')  
    elif hand == 'Pointing_Up':
        print('\U0001F446')  
    elif hand == 'Thumb_Down':
        print('\U0001F44E')  
    elif hand == 'Thumb_Up':
        print('\U0001F44D')  
    elif hand == 'Victory':
        print('\u270C')  
    elif hand == 'ILoveYou':
        print('\U0001FAF6')"""


#Create an GestureRecognizer object.
base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)



try:
    while True:
        data, image = cap.read()
        if not data:
            continue  # Skip the rest of the loop if frame capture failed
        # Image processing
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # Draw landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                )

        cv2.imshow('Hand Tracker', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

        # Gesture recognition and emoji output
        if results.multi_hand_landmarks:
            top_gesture = results.multi_hand_landmarks[0]  # Assuming the first found hand
            emoji(top_gesture.category_name)  # This will not work directly; placeholder for real implementation

        input("Press Enter to capture next gesture...")  # Wait for user input to continue

finally:
    cap.release()
    cv2.destroyAllWindows()