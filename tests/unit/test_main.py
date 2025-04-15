from main import app
from main import root, visits, visit, hello, hello_form
from hamcrest import assert_that, equal_to

# Unit test for the functions: def root() def visits() (Detelina)














# Unit test for the functions: def visit(visit_id) def hello() (Shaheera)
 












# Unit test for the function: def hello_form()(Mehdi)
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














