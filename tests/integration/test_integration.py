import pytest
import re
import json, html
from main import app
from hamcrest import assert_that, equal_to, contains_string
from datetime import datetime

# Integration test for "Add Visit Flow" (Tester: Mehdi):

#Fixture to ensure the app is running and provide a requests session.
@pytest.fixture
def client():
    # Configure the app for testing

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
        assert visit_id in found_visit_ids, f"Visit ID {visit_id} not found in /visits"



#Detelina tests
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

# Integration tests for the routes /visits and visits/<id> (Tester: Shaheera)

def test_visits_without_parameters_should_return_all_visits(client):
   
    response = client.get("/visits")

    assert_that(response.status_code, equal_to(200))

#Test case: If a range of date is provided, it should display the results only within that range
def test_visits_with_valid_dates_should_return_visits_in_that_range(client):
    # Simulate visit
    client.get("/", environ_base={
        "REMOTE_ADDR": "127.0.0.2",
        "HTTP_USER_AGENT": "filter-test-user"
    })

    # Date filter (today)
    today = datetime.now().strftime("%Y-%m-%d")

    # GIVEN /visits is called 
    # WHEN a range of date is provided 
    response = client.get(f"/visits?from={today}&to={today}")
    assert_that(response.status_code, equal_to(200))

    # Parse response
    visits_data = json.loads(response.get_data(as_text=True))
    print("\n==== VISITS DATA ====\n", visits_data)

    # THEN visits within the range should be shown
    found = any("filter-test-user" in visit["user_agent"] for visit in visits_data)
    assert found, "Expected 'filter-test-user' in the visits list"


def test_visits_with_invalid_from_date_should_return_404(client):

    # GIVEN /visits is called
    # WHEN an invalid from date is provided
    response = client.get("/visits?from=not-a-date")
    decoded = html.unescape(response.get_data(as_text=True))

    # THEN it should return a 404 with an error message
    assert_that(response.status_code, equal_to(400))
    assert_that(decoded, contains_string("Invalid 'from' date format"))

def test_visits_with_invalid_to_date_should_return_404(client):
  
     # GIVEN /visits is called
    # WHEN an invalid from date is provided
    response = client.get("/visits?to=not-a-date")
    decoded = html.unescape(response.get_data(as_text=True))

    # THEN it should return a 404 with an error message
    assert_that(response.status_code, equal_to(400))
    assert_that(decoded, contains_string("Invalid 'to' date format"))
