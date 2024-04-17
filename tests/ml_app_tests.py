
import pytest
from unittest.mock import patch, MagicMock
from base64 import b64encode
import os
import json

@pytest.fixture
def app():
    # Mocking the GestureRecognizer to prevent file access
    with patch('mediapipe.tasks.vision.GestureRecognizer.create_from_options', return_value=MagicMock()) as mock_recognizer:
        from machine_learning_client.app import app as flask_app
        flask_app.config.update({
            "TESTING": True,
            "MONGODB_SETTINGS": {
                'alias': 'default',
                'host': 'mongomock://localhost'
            }
        })
        yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    from pymongo import MongoClient
    monkeypatch.setattr('pymongo.MongoClient', MongoClient)
    mock_client = MongoClient()
    db = mock_client.db
    monkeypatch.setattr('machine_learning_client.app.mongo_client', mock_client)
    monkeypatch.setattr('machine_learning_client.app.db', db)
    return db

# Test the response for different gestures to ensure accuracy
@pytest.mark.parametrize("gesture, expected", [
    ("Closed_Fist", "\u270A"),
    ("Open_Palm", "\u270B"),
    ("Victory", "\u270C"),
    ("Thumb_Down", "\U0001F44E"),
    ("Thumb_Up", "\U0001F44D"),
    ("Pointing_Up", "\U0001F446"),
    ("ILoveYou", "\U0001F91F"),
    (None, "\U0001FAE5")  
])
def test_gesture_to_emoji_conversion(gesture, expected, app):
    from machine_learning_client.app import emoji
    result = emoji(gesture)
    assert result == expected

# Test the /process_img route
def test_process_img_route(client):
    image_data = b64encode(b"mock_image_data").decode('utf-8')
    
    response = client.post('/process_img', json={'image': image_data})
    
    assert response.status_code == 500

# Test database connection
def test_database_connection():
    from machine_learning_client.app import gestureDB
    assert gestureDB is not None

