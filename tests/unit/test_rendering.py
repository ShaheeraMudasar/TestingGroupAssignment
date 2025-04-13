import unittest
from unittest.mock import patch

import rendering

class TestRenderingFunctions(unittest.TestCase):

    # Test: format_welcome_message with a valid visit
    @patch("rendering.to_basic_html_page")
    def test_format_welcome_message_valid(self, mock_to_basic):
        # Given
        visit = {'id': 42}
        mock_to_basic.return_value = "<html>Mock</html>"

        # When
        result = rendering.format_welcome_message(visit)

        # Then
        mock_to_basic.assert_called_once_with("Welcome", "Welcome, you are visitor number 42")
        self.assertEqual(result, "<html>Mock</html>")

    # Test: format_welcome_message with empty dict (boundary case)
    @patch("rendering.to_basic_html_page")
    def test_format_welcome_message_missing_id(self, mock_to_basic):
        # Given an invalid visit dictionary (missing 'id')
        visit = {}

        # When/Then
        with self.assertRaises(KeyError):  # Boundary case: missing required key
            rendering.format_welcome_message(visit)

    # Test: format_visit_history with valid history
    @patch("rendering.get_html_end_block", return_value="</end>")
    @patch("rendering.get_html_start_block", return_value="<start>")
    @patch("rendering.to_text_paragraph", side_effect=lambda x: f"<p>{x}</p>")
    @patch("rendering.to_heading_line", return_value="<h1>Visit history</h1>")
    def test_format_visit_history_valid(self, mock_heading, mock_para, mock_start, mock_end):
        # Given a list of visits
        history = [{'id': 1, 'timestamp': '2024-01-01'}, {'id': 2, 'timestamp': '2024-01-02'}]

        # When
        result = rendering.format_visit_history(history)

        # Then
        self.assertTrue(result.startswith("<start>"))
        self.assertIn("<h1>Visit history</h1>", result)
        self.assertIn("<p>- 2024-01-01: Visit #1\n</p>", result)
        self.assertIn("<p>- 2024-01-02: Visit #2\n</p>", result)
        self.assertTrue(result.endswith("</end>"))

    # Test: format_visit_history with empty list (edge case)
    @patch("rendering.get_html_end_block", return_value="</end>")
    @patch("rendering.get_html_start_block", return_value="<start>")
    @patch("rendering.to_text_paragraph", side_effect=lambda x: f"<p>{x}</p>")
    @patch("rendering.to_heading_line", return_value="<h1>Visit history</h1>")
    def test_format_visit_history_empty(self, *_):
        # Given an empty history list
        history = []

        # When
        result = rendering.format_visit_history(history)

        # Then: Only the title and start/end blocks should be present
        self.assertIn("<h1>Visit history</h1>", result)
        self.assertNotIn("<p>", result.replace("<h1>Visit history</h1>", ""))

    # Test: format_visit_details with valid visit
    @patch("rendering.get_html_end_block", return_value="</end>")
    @patch("rendering.get_html_start_block", return_value="<start>")
    @patch("rendering.to_text_paragraph", side_effect=lambda x: f"<p>{x}</p>")
    @patch("rendering.to_heading_line", return_value="<h1>Visit #1</h1>")
    def test_format_visit_details_valid(self, *_):
        # Given
        visit = {
            'id': 1,
            'timestamp': '2024-01-01',
            'ip': '127.0.0.1',
            'user_agent': 'Mozilla/5.0'
        }

        # When
        result = rendering.format_visit_details(visit)

        # Then
        self.assertIn("<h1>Visit #1</h1>", result)
        self.assertIn("<p>When: 2024-01-01</p>", result)
        self.assertIn("<p>IP: 127.0.0.1</p>", result)
        self.assertIn("<p>User agent: Mozilla/5.0</p>", result)