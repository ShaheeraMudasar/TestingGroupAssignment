import pytest
from datetime import datetime
from main import app

# Integration Tests for the "Add Visit Flow"; practicing DB insert & readback (Mehdi):

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# (1) Test submitting a visit (from root or the /submit route); and ensuring it is stored in the DB by confirming it is shown in /visits endpoint.

def visit_data():
    """Fixture that provides sample visit data for testing."""
    return {
        "ip": "127.0.0.1",
        "user_agent": "Mozilla/5.0",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def test_submit_visit(client, visit_data):

    # Given: A sample visit data
    url = '/submit'
    data = visit_data
    
    # When: I send a POST request to the /submit endpoint to add a visit
    response = client.post(url, json=data)
    
    # Then: I should receive a 201 status code (Created) here; and later on the next line: the visit should be shown in /visits
    assert response.status_code == 201
    
    # Now, check if the visit is displayed in /visits
    visits_url = '/visits'
    response = client.get(visits_url)
    
    # Check if the visit appears in the visit list
    assert response.status_code == 200
    assert data['ip'] in response.get_data(as_text=True)  # Assuming IP is shown in the visit list
    assert data['user_agent'] in response.get_data(as_text=True)  # Assuming user agent is shown


# (2) Test adding multiple visits; and ensuring they all appear in the /visits endpoint.

def test_add_multiple_visits(client, visit_data):

    # Given: Multiple visits sample data
    visits = [
        {"ip": "127.0.0.1", "user_agent": "Mozilla/5.0", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        {"ip": "192.168.0.1", "user_agent": "Chrome/91.0", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        {"ip": "10.0.0.1", "user_agent": "Safari/12.1", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    ]
    
    # When: I send several POST requests to the /submit endpoint
    for visit in visits:
        response = client.post('/submit', json=visit)
        assert response.status_code == 201  # Check for successful creation
    
    # Then: I should retrieve the /visits list and confirm all visits appear
    visits_url = '/visits'
    response = client.get(visits_url)
    
    # Check if each visit appears in the visit list
    for visit in visits:
        assert visit['ip'] in response.get_data(as_text=True)
        assert visit['user_agent'] in response.get_data(as_text=True)





import pytest
import requests
import re

# Base URL for the Flask app (from docker-compose-test.yml)
BASE_URL = "http://localhost:5100"

@pytest.fixture
def client():
    """Fixture to ensure the app is running and provide a requests session."""
    session = requests.Session()
    # Verify the app is up
    response = session.get(BASE_URL)
    assert response.status_code == 200, "Flask app is not running"
    return session

def test_add_single_visit(client):
    """Test that a visit to / adds a record and it appears in /visits."""
    # Step 1: Hit the root endpoint to record a visit
    root_response = client.get(BASE_URL)
    assert root_response.status_code == 200, "Root endpoint failed"

    # Extract visit ID from the welcome message using regex
    welcome_text = root_response.text
    match = re.search(r"Welcome, you are visitor number (\d+)", welcome_text)
    assert match, "Unexpected welcome message format"
    visit_id = int(match.group(1))  # Extract the visit ID (e.g., 1)

    # Step 2: Check /visits to confirm the visit is listed
    visits_response = client.get(f"{BASE_URL}/visits")
    assert visits_response.status_code == 200, "/visits endpoint failed"

    # Check for Visit #<id> in the response
    visits_text = visits_response.text
    assert f"Visit #{visit_id}" in visits_text, f"Visit #{visit_id} not found in /visits"

def test_add_multiple_visits(client):
    """Test that multiple visits to / are recorded and all appear in /visits."""
    # Step 1: Record three visits
    visit_ids = []
    for _ in range(3):
        root_response = client.get(BASE_URL)
        assert root_response.status_code == 200, "Root endpoint failed"
        welcome_text = root_response.text
        match = re.search(r"Welcome, you are visitor number (\d+)", welcome_text)
        assert match, "Unexpected welcome message format"
        visit_id = int(match.group(1))
        visit_ids.append(visit_id)

    # Step 2: Check /visits to confirm all visits are listed
    visits_response = client.get(f"{BASE_URL}/visits")
    assert visits_response.status_code == 200, "/visits endpoint failed"

    # Verify all visit IDs appear in the response
    visits_text = visits_response.text
    for visit_id in visit_ids:
        assert f"Visit #{visit_id}" in visits_text, f"Visit #{visit_id} not found in /visits"