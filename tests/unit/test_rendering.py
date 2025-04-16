import unittest
from unittest.mock import patch
from hamcrest import assert_that, equal_to
import pytest
import rendering
from rendering import format_visit_history, format_hello_greeting, format_visit_details

# Unit tests for functionde format_visit_history(history) (Mehdi)

# This function gets a list of visit dictionaries and formats them into an HTML string.
# It uses helper functions to create the HTML structure:
# "get_html_start_block", "to_heading_line", "to_text_paragraph", and "get_html_end_block".
# Our test should Mock these functions to ensure that the output of "format_visit_history" is as expected.

# The function format_visit_history uses helper functions to generate full HTML strings.
# First we mock these helper functions to isolate the tes.
# We can also mock the visit dictionary or a simpler approch is to buil a sample visit dictionary.
@patch("rendering.get_html_end_block")
@patch("rendering.to_text_paragraph")
@patch("rendering.to_heading_line")
@patch("rendering.get_html_start_block")
def test_format_visit_history(mock_start, mock_heading, mock_paragraph, mock_end):
    # Given: mock HTML helper functions and sample visit history
    mock_start.return_value = "<html>"
    mock_heading.return_value = "<h1>Visit history</h1>"
    mock_paragraph.side_effect = [
        "<p>- 2025-04-14 12:00:00: Visit #1</p>",
        "<p>- 2025-04-15 13:00:00: Visit #2</p>"
    ]
    mock_end.return_value = "</html>"
    
    visit_history = [
        {"id": 1, "timestamp": "2025-04-14 12:00:00"},
        {"id": 2, "timestamp": "2025-04-15 13:00:00"}
    ]

    # When: calling the function format_visit_history
    result = format_visit_history(visit_history)

    # Then: it should return correctly formatted HTML with all pieces
    expected = (
        "<html>"
        "<h1>Visit history</h1>"
        "<p>- 2025-04-14 12:00:00: Visit #1</p>"
        "<p>- 2025-04-15 13:00:00: Visit #2</p>"
        "</html>"
    )
    assert_that(result, equal_to(expected))


# def format_visit_details(visit) (Detelina)

@patch("rendering.get_html_end_block", return_value="End")
@patch("rendering.to_text_paragraph", return_value="Paragraph")
@patch("rendering.to_heading_line", return_value="Heading")
@patch("rendering.get_html_start_block", return_value="Start")
def test_format_visit_details_normal(mock_start, mock_heading, mock_paragraph, mock_end ):
    visit = {
    "id": 1,
    "timestamp": "2025-01-01 12:00:00",
    "ip": "127.0.0.1",
    "user_agent": "Chrome"
}
    result = format_visit_details(visit)
    expected = "StartHeadingParagraphParagraphParagraphEnd"
    assert result == expected

  
@patch("rendering.get_html_end_block", return_value="End")
@patch("rendering.to_text_paragraph", return_value="Paragraph")
@patch("rendering.to_heading_line", return_value="Heading")
@patch("rendering.get_html_start_block", return_value="Start")
def test_format_visit_details_missing_data(mock_start, mock_heading, mock_paragraph, mock_end ):
    visit = {
    "id": "2",
    "timestamp": "2025-01-01 12:00:00",
    "ip": "",
    "user_agent": "Chrome"
}
    result = format_visit_details(visit)
    expected = "StartHeadingParagraphParagraphParagraphEnd"
    assert result == expected

  











#def format_hello_greeting(name) (Shaheera)