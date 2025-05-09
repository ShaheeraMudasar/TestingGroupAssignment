from html_utils import to_basic_html_page, to_error_message, get_html_start_block, get_html_end_block, to_heading_line, to_text_paragraph
import pytest
from unittest.mock import patch
from hamcrest import assert_that, equal_to

# Unit tests for functions: get_html_start_block, get_html_end_block (Tester: Mehdi)

# (1) get_html_start_block:

# # Test Case: get_html_start_block should return a correct HTML start block
# This is an equivalence class test for checking the function with valid input

@patch("html_utils.get_html_start_block", return_value="<!DOCTYPE html>\n<html lang=\"en\">\n<head><meta charset=\"UTF-8\"><title>Page</title></head>\n<body>\n")
def test_get_html_start_block(mock_get_html_start):
    # Given a valid HTML start block
    # When get_html_start_block is called
    start_block = get_html_start_block()    
    # Then the returned HTML should match the expected HTML start block
    expected_output = "<!DOCTYPE html>\n<html lang=\"en\">\n<head><meta charset=\"UTF-8\"><title>Page</title></head>\n<body>\n"
    assert_that(start_block, equal_to(expected_output))

# Boundary Test Case: get_html_start_block should still return a valid start block even when input is empty
# This checks if the function handles empty input (Boundary Test).
@patch("html_utils.get_html_start_block", return_value="<!DOCTYPE html>\n<html lang=\"en\">\n<head><meta charset=\"UTF-8\"><title>Page</title></head>\n<body>\n")
def test_get_html_start_block_empty(mock_get_html_start):
    # Given an empty title for the HTML start block
    # When get_html_start_block is called
    start_block = get_html_start_block()
    # Then the returned HTML should contain a title tag with empty content
    expected_output = "<!DOCTYPE html>\n<html lang=\"en\">\n<head><meta charset=\"UTF-8\"><title>Page</title></head>\n<body>\n"
    assert_that(start_block, equal_to(expected_output))

# Edge Test Case: get_html_start_block should still return a valid start block even when input is None
# This  checks if the function  handles `None` input (Edge Case).
@patch("html_utils.get_html_start_block", return_value="<!DOCTYPE html>\n<html lang=\"en\">\n<head><meta charset=\"UTF-8\"><title>Page</title></head>\n<body>\n")
def test_get_html_start_block_none(mock_get_html_start):
    # Given `None` as the title for the HTML start block
    # When get_html_start_block is called
    start_block = get_html_start_block()
    # Then the returned HTML should contain `None` as the title
    expected_output = "<!DOCTYPE html>\n<html lang=\"en\">\n<head><meta charset=\"UTF-8\"><title>Page</title></head>\n<body>\n"
    assert_that(start_block, equal_to(expected_output))

# (2) get_html_end_block:

# Test Case: get_html_end_block should return a correct HTML end block
# This is an equivalence class test for checking the function with valid input
@patch("html_utils.get_html_end_block", return_value="</body>\n</html>\n")
def test_get_html_end_block(mock_get_html_end):
    # Given a valid HTML end block
    # When get_html_end_block is called
    end_block = get_html_end_block()
    # Then the returned HTML should match the expected HTML end block
    expected_output = "</body>\n</html>\n"
    assert_that(end_block, equal_to(expected_output))

# Boundary Test Case: get_html_end_block should still return a valid end block even with empty content
# This checks if the function handles empty input (Boundary Test).
@patch("html_utils.get_html_end_block", return_value="</body>\n</html>\n")
def test_get_html_end_block_empty(mock_get_html_end):
    # Given an empty body for the HTML end block
    # When get_html_end_block is called
    end_block = get_html_end_block()
    # Then the returned HTML should still be a valid closing HTML tag
    expected_output = "</body>\n</html>\n"
    assert_that(end_block, equal_to(expected_output))

# Edge Test Case: get_html_end_block shoudl still return a valid end block even when input is None
# This checks if the function handles `None` input (Edge Case).
@patch("html_utils.get_html_end_block", return_value="</body>\n</html>\n")
def test_get_html_end_block_none(mock_get_html_end):
    # Given `None` as the content for the HTML end block
    # When get_html_end_block is called
    end_block = get_html_end_block()
    # Then the returned HTML should be a valid closing HTML tag
    expected_output = "</body>\n</html>\n"
    assert_that(end_block, equal_to(expected_output))
 # Unit tests for functions: to_heading_line, to_text_paragraph

def test_to_heading_line_2():
    heading = to_heading_line("Hello", 2)
    expected = "<h2>Hello</h2>\n"
    assert heading == expected

def test_to_heading_line_3():
    heading = to_heading_line("Hello again", 3)
    expected = "<h3>Hello again</h3>\n"
    assert heading == expected

def test_to_heading_line_char():
    heading = to_heading_line("<Hello> & <b>Goodbye<b>", 1)
    expected = "<h1>&lt;Hello&gt; &amp; &lt;b&gt;Goodbye&lt;b&gt;</h1>\n"
    assert heading == expected

def test_to_heading_line_empty():
    heading = to_heading_line("", 1)
    expected = "<h1></h1>\n"
    assert heading == expected


def test_to_text_paragraph_empty():
    text = to_text_paragraph("")
    expected = "<p></p>\n"
    assert text == expected

def test_to_text_paragraph_char():
    text = to_text_paragraph("<> &")
    expected = "<p>&lt;&gt; &amp;</p>\n"
    assert text == expected





# Unit tests for functions: to_error_message, to_basic_html_page (Tester: Shaheera)

from html_utils import to_basic_html_page, to_error_message, get_html_start_block, get_html_end_block, to_heading_line, to_text_paragraph
import pytest
from unittest.mock import patch
from hamcrest import assert_that, equal_to

# Test Case: to_error_message should format an error page using to_basic_html_page
# This is an equivalence class test for checking the function with valid input
@patch("html_utils.to_basic_html_page", return_value="<html>Error Page</html>")
def test_to_error_message(mock_to_basic):
    # Run the function with test input
    html = to_error_message("Something broke")

    # Check the returned HTML is as mocked
    assert_that(html, equal_to("<html>Error Page</html>"))

# Test Case: to_error_message should return None as text if the input given is None
# This is an equivalence class test for checking the function with None input
@patch ("html_utils.to_basic_html_page", return_value="<html>Error Page</html>")
def test_to_error_message_with_none_text(mock_to_basic):
    html = to_error_message(None)
    assert_that(html, equal_to("<html>Error Page</html>"))

# Test Case: to_error_message should return a long text on html page when the input is long
# This is a boundary test for checking the function with long text input
@patch("html_utils.to_basic_html_page", return_value="<html>Error Page</html>")
def test_to_error_message_with_long_text(mock_to_basic):
    long_text = "This is a very long error message that should be displayed on the HTML page." * 10
    html = to_error_message(long_text)
    assert_that(html, equal_to("<html>Error Page</html>"))

# Test Case: to_error_message should rerturn full html with empty paragraph
# This is a boundary test for checking the function with empty input
@patch("html_utils.to_basic_html_page", return_value="<html><p></p></html>")
def test_to_error_message_with_empty_paragraph(mock_to_basic):
    html = to_error_message("")
    assert_that(html, equal_to("<html><p></p></html>"))

# Test Case: to_basic_html_page should return a complete HTML page with title, heading and text
# This test ensures the function returns the correct HTML structure with the given inputs (An Equivalence Class test)

@patch("html_utils.get_html_start_block", return_value="HTML-Start")
@patch("html_utils.to_heading_line", return_value="<h2>Mock-Heading</h2>")
@patch("html_utils.to_text_paragraph", return_value="<p>Mock-Paragraph</p>")
@patch("html_utils.get_html_end_block", return_value="HTML-End")
def test_to_basic_html_page_with_heading(mock_start, mock_heading, mock_paragraph, mock_end):
    html = to_basic_html_page("Test Title", "Test Text", "Test Heading")

    expected = "HTML-Start<h2>Mock-Heading</h2><p>Mock-Paragraph</p>HTML-End"
    assert_that(html, equal_to(expected))

# test case: to_basic_html_page_without_heading should return a complete HTML page without heading
# This test ensures the function returns the correct HTML structure without a heading (An Equivalence Class test with missing parameter)

@patch("html_utils.get_html_end_block", return_value="HTML-End")
@patch("html_utils.to_text_paragraph", return_value="<p>Mock-Paragraph</p>")
@patch("html_utils.get_html_start_block", return_value="HTML-Start")



def test_to_basic_html_page_without_heading(mock_start, mock_paragraph, mock_end):
    # Run the function with test input
    html = to_basic_html_page("Test Title", "Test Text")

    # Check the returned HTML is as expected
    expected = "HTML-Start<p>Mock-Paragraph</p>HTML-End"
    assert_that(html, equal_to(expected))

# test case: to_basic_html_page_with_no_text should return a complete HTML page with title and no text
# this is a eqivalence class test 
@patch("html_utils.get_html_end_block", return_value="HTML-End")
@patch("html_utils.to_text_paragraph", return_value="<p></p>")
@patch("html_utils.to_heading_line", return_value="<h2>Mock-Heading</h2>")
@patch("html_utils.get_html_start_block", return_value="HTML-Start")


def test_to_basic_html_page_with_no_text(mock_start, mock_headine, mock_paragraph, mock_end):
    html = to_basic_html_page("Test Title", None, "Test Heading")
    expected = "HTML-Start<h2>Mock-Heading</h2><p></p>HTML-End" 

    assert_that(html, equal_to(expected))

# test case: to_basic_html_page_with_a_long_text should return a complete HTML page with long text
# this is a boundary test 
@patch("html_utils.get_html_end_block", return_value="HTML-End")
@patch("html_utils.to_text_paragraph", return_value="<p>Mock-Paragraph</p>")
@patch("html_utils.to_heading_line", return_value="<h2>Mock-Heading</h2>")
@patch("html_utils.get_html_start_block", return_value="HTML-Start")

def test_to_basic_html_page_with_a_long_text(mock_start, mock_heading, mock_paragraph, mock_end):
    long_text = "This is a very long text that should be wrapped in a paragraph tag." * 10
    html = to_basic_html_page("Test Title", long_text, "Test Heading")
    expected = "HTML-Start<h2>Mock-Heading</h2><p>Mock-Paragraph</p>HTML-End" 

    assert_that(html, equal_to(expected))



