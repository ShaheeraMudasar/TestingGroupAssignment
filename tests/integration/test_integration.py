import pytest
import re
import json
from main import app
# Integration test for "Add Visit Flow" (Tester: Mehdi):

#Fixture to ensure the app is running and provide a requests session.
@pytest.fixture
def client():
    # Configure the app for testing
    from main import app
    app.config["TESTING"] = True
    # Use the test client without reinitializing the database
    with app.test_client() as client:
        yield client

# (1) Test that a visit to / adds a record in the DB and it appears in /visits."

def test_add_single_visit(client):
    # Step 1: Simulate a GET request to / to record a visit
    root_response = client.get("/", environ_base={"REMOTE_ADDR": "127.0.0.1", "HTTP_USER_AGENT": "test-agent"})
    assert root_response.status_code == 200, "Root endpoint failed"

    # Extract visit ID from the welcome message using regex
    welcome_text = root_response.get_data(as_text=True)
    match = re.search(r"Welcome, you are visitor number (\d+)", welcome_text)
    assert match, "Unexpected welcome message format"
    visit_id = int(match.group(1))  # Extract the visit ID (e.g., 1)

    # Step 2: Simulate a GET request to /visits to check the visit
    visits_response = client.get("/visits")
    assert visits_response.status_code == 200, "/visits endpoint failed"

    # Parse JSON response and check for visit_id
    visits_text = visits_response.get_data(as_text=True)
    try:
        visits_data = json.loads(visits_text)
    except json.JSONDecodeError:
        assert False, "Expected JSON response from /visits"
    visit_ids = [visit["id"] for visit in visits_data]
    assert visit_id in visit_ids, f"Visit ID {visit_id} not found in /visits"

# (2) Test that multiple visits to / are recorded and all appear in /visits.
def test_add_multiple_visits(client):
    """Test that multiple visits to / are recorded and all appear in /visits."""
    # Step 1: Simulate three GET requests to /
    visit_ids = []
    for i in range(3):
        root_response = client.get("/", environ_base={"REMOTE_ADDR": f"127.0.0.{i+1}", "HTTP_USER_AGENT": f"test-agent-{i}"})
        assert root_response.status_code == 200, "Root endpoint failed"
        welcome_text = root_response.get_data(as_text=True)
        match = re.search(r"Welcome, you are visitor number (\d+)", welcome_text)
        assert match, "Unexpected welcome message format"
        visit_id = int(match.group(1))
        visit_ids.append(visit_id)

    # Step 2: Simulate a GET request to /visits
    visits_response = client.get("/visits")
    assert visits_response.status_code == 200, "/visits endpoint failed"

    # Parse JSON response and check for all visit_ids
    visits_text = visits_response.get_data(as_text=True)
    try:
        visits_data = json.loads(visits_text)
    except json.JSONDecodeError:
        assert False, "Expected JSON response from /visits"
    found_visit_ids = [visit["id"] for visit in visits_data]
    for visit_id in visit_ids:
        assert visit_id in found_visit_ids, f"Visit ID {visit_id} not found in /visits"from main import app

def test_hello_form_loads():
    client = app.test_client()
    response = client.get("/hello-form")

    assert response.status_code == 200
    assert "<form" in response.get_data(as_text=True)
    assert 'name="name"' in response.get_data(as_text=True)


def test_hello_query_greeting():
    client = app.test_client()
    response = client.get("/hello?name=Alice")

    assert response.status_code == 200
    assert "Hello, Alice" in response.get_data(as_text=True)

    