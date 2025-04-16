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