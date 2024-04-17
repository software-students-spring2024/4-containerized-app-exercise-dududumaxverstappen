# web_app_tests

import pytest
from web_app.app import app as flask_app 

@pytest.fixture
def app():
    app = flask_app
    app.config.update({
        "TESTING": True, 
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_home_page_load(client):
    """
    Test that the home page loads correctly
    """
    response = client.get('/')
    assert response.status_code == 200

def test_get_emoji(client):
    """
    Test the /get_emoji route
    """
    response = client.get("/get_emoji")
    assert response.status_code == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.data.decode() in ["\U0001FAE5", "\u270A", "\u270B", "\U0001F446", "\U0001F44E", "\U0001F44D", "\u270C", "\U0001F91F", "\U00002753"]

def test_results_page(client):
    """
    Test the results page
    """
    response = client.get("/results")
    assert response.status_code == 200
    assert "text/html" in response.content_type
    assert "Emojis" in response.data.decode()

def test_404_page(client):
    """
    Test that a non-existent route provides a 404 status code.
    """
    response = client.get('/nothing-here')
    assert response.status_code == 404


def test_database_connection():
    """
    Test database connection setup
    """
    from web_app.app import gestureDB
    assert gestureDB is not None

def test_additional_route(client):
    """
    Test additional route
    """
    response = client.get("/additional_route")
    assert response.status_code == 404  

def test_invalid_input(client):
    """
    Test invalid input handling
    """
    response = client.post("/submit_data", data={"invalid_field": "invalid_value"})
    assert response.status_code == 404  

def test_database_connection_failure(monkeypatch):
    """
    Test database connection failure
    """
    import web_app.app
    
    def mock_mongo_client(*args, **kwargs):
        raise Exception("Mock MongoDB connection failure")

    monkeypatch.setattr(web_app.app, 'MongoClient', mock_mongo_client)
    with pytest.raises(Exception):
        web_app.app.mongo_client = web_app.app.MongoClient('mongodb+srv://mockuser:mockpassword@mockhost/mockdatabase')

def test_emoji(client):
    """
    Test emoji
    """
    from web_app.app import gestureDB
    
    invalid_data = {'result': {'top_gesture': 'Invalid_Gesture'}}
    gestureDB.insert_one({'result': {'top_gesture': 'Invalid_Gesture'}})
    
    response = client.get("/get_emoji")
    assert response.status_code == 200
    assert response.content_type == "text/plain; charset=utf-8"

