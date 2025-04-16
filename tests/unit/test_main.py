from main import app, root, visits, visit, hello, hello_form
from hamcrest import assert_that, equal_to
from unittest.mock import patch
from flask import Flask, request

# Unit test for the functions: def root() def visits() (Detelina)
@patch("main.format_welcome_message")
@patch("main.add_visit")
def test_root(mock_add_visit, mock_format_welcome_message):
    mock_add_visit.return_value= {"id": 1}
    mock_format_welcome_message.return_value="<h1> User-Agent unknown</h1>\n"
    client = app.test_client()
    response = client.get("/")

    expected_html_fragment = "<h1> User-Agent unknown</h1>\n"
    assert_that(response.status_code, equal_to(200))
    assert_that(expected_html_fragment in response.get_data(as_text=True), equal_to(True))



@patch("main.format_visit_history")
@patch("main.to_error_message")
@patch("main.get_all_visits")
def test_visits(mock_get_all_visits, mock_to_error_message, mock_format_visit_history):
    mock_get_all_visits.return_value=[{"id": 1, "timestamp": "2025-01-01 12:00:00", "ip": "127.0.0.1", "user_agent": "Chrome"}]
    mock_to_error_message.return_value="Error"
    mock_format_visit_history.return_value= ("<html>"
        "<h1>Visit History</h1>"
        "<p>- 2025-04-14 12:00:00: Visit #1</p>"
        "<p>- 2025-04-15 13:00:00: Visit #2</p>"
        "</html>" )
    client = app.test_client()
    response = client.get("/visits")
    
    assert response.status_code == 200
    assert "<h1>Visit History</h1>" in response.get_data(as_text=True)

@patch("main.format_visit_history")
@patch("main.to_error_message")
@patch("main.get_all_visits")
def test_visits_wrong_format(mock_get_all_visits, mock_to_error_message, mock_format_visit_history):
    mock_get_all_visits.return_value=[{"id": 1, "timestamp": "2025-01-01 12:00:00", "ip": "127.0.0.1", "user_agent": "Chrome"}]
    mock_to_error_message.return_value="Error"
    mock_format_visit_history.return_value= ("<html>"
        "<h1>Visit History</h1>"
        "<p>- 2025-04-14 12:00:00: Visit #1</p>"
        "<p>- 2025-04-15 13:00:00: Visit #2</p>"
        "</html>" )
    client = app.test_client()
    response = client.get("/visits?from=banana")
    
    assert response.status_code == 400
    assert "Error" in response.get_data(as_text=True)

@patch("main.format_visit_history")
@patch("main.to_error_message")
@patch("main.get_all_visits")
def test_visits_empty(mock_get_all_visits, mock_to_error_message, mock_format_visit_history):
    mock_get_all_visits.return_value=[]
    mock_to_error_message.return_value="Error"
    mock_format_visit_history.return_value= ("<html><h1>Visit History</h1><p>No visits</p></html>" )
    client = app.test_client()
    response = client.get("/visits")
    
    assert response.status_code == 200
    assert "<h1>Visit History</h1>" in response.get_data(as_text=True)




# Unit test for the functions: def visit(visit_id) def hello() (Tester: Shaheera)
@patch("main.get_visit_by_id", 
       return_value = {"id": "1",
       "timestamp": "2025-01-01", 
       "ip": "127.0.0.1", "user_agent":"testAgent"})
@patch("main.format_visit_history", return_value = "Visit details")

# Test Case: When visit id exists 
def test_visit_by_id_returns_detail_about_that_visit(mock_format, mock_get_visit): 
    client = app.test_client()

    # WHEN visit id is provided
    response = client.get("/visit/1")
    # THEN it should return visit details against that id
    assert_that(response.get_data(as_text = True), contains_string("Visit details"))

# Test case: When the visit id is not found
@patch("main.get_visit_by_id", 
       return_value = None)
@patch("main.format_visit_history", return_value = "Visit not found")

def test_visit_by_id_should_return_404_when_no_visit_found(mock_get_visit, mock_format):
    client = app.test_client()
    # WHEN an invalid id is provided
    response = client.get ("/visit/999")
    # THEN it throws a 404 error with a message
    assert_that(response.status_code, equal_to(404))
    assert_that(response.get_data(as_text = True), contains_string("Visit not found"))

# Test Case: When a name is provided in the web-form
@patch("main.format_hello_greeting", return_value = "Hello Alice!")
def test_hello_returns_greetings(mock_format_hello_greeting):
    client = app.test_client()
    # WHEN name is provided 
    response = client.get ("/hello?name=Alice")
    # THEN greetings are displayed for that name
    assert_that(response.get_data(as_text = True), contains_string("Hello Alice!"))
    

# Unit test for the function: def hello_form()(Tester: Mehdi)
# The function hello_form() renders a simple static HTML form that lets users input their name and submit it.
# It includes a test field for the name and a submit button.
# We use Flask's built-in test_client() to simulate requests.
# We are not mocking the database or any other external dependencies.
 
    # IMPORTANT: THE BUG IN THE HTML FORM
    # Missing Attribute: The <input> is missing a name="name" attribute, which means no value will be passed to /hello when the form is submitted.

        # Line 54 in the source code:
        # <input type="text" id="name"><br><br>
        # SHOULD BE:
        # <input type="text" id="name" name="name"><br><br>

# The test should verify taht route returns the expected HTML form.

def test_hello_form_returns_html_form():
    # Given: a test client for the Flask app
    client = app.test_client()

    # When: making a GET request to the /hello-form route
    response = client.get("/hello-form")

    # Then: response should contain the expected HTML form
    expected_html_fragment = "<h1>Say Hello</h1>"
    assert_that(response.status_code, equal_to(200))
    assert_that(expected_html_fragment in response.get_data(as_text=True), equal_to(True))














