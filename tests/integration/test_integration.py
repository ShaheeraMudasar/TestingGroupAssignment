import pytest
import re
import os
from main import app, root, visits, visit, hello, hello_form

# Set environment variables for the test database (matching .env.test)
os.environ["DB_HOST"] = "test_db"
os.environ["DB_PORT"] = "5432"
os.environ["DB_NAME"] = "postgres"
os.environ["DB_USER"] = "postgres"
os.environ["DB_PASSWORD"] = "password"

@pytest.fixture
def client():
    """Fixture to provide a Flask test client and initialize the database."""
    # Configure the app for testing
    app.config["TESTING"] = True
    # Initialize the database
    from db import init_db
    init_db()
    # Create a test client
    with app.test_client() as client:
        yield client

def test_add_single_visit(client):
    """Test that a visit to / adds a record and it appears in /visits."""
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

    # Check for Visit #<id> in the response
    visits_text = visits_response.get_data(as_text=True)
    assert f"Visit #{visit_id}" in visits_text, f"Visit #{visit_id} not found in /visits"

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

    # Verify all visit IDs appear in the response
    visits_text = visits_response.get_data(as_text=True)
    for visit_id in visit_ids:
        assert f"Visit #{visit_id}" in visits_text, f"Visit #{visit_id} not found in /visits"