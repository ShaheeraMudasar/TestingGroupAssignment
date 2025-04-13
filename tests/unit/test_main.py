
# PYTHONPATH=$(pwd) pytest tests/unit/test_main.py

import unittest
from unittest import mock
from unittest.mock import patch, MagicMock
from main import app, root, visits, visit, hello, hello_form
from db import get_visit_by_id, add_visit, get_all_visits, init_db
from rendering import format_visit_details, format_welcome_message, format_hello_greeting
from html_utils import to_error_message
from datetime import datetime
from flask import jsonify
import psycopg2
import sys
import os
os.environ['FLASK_ENV'] = 'testing' # Make sure we are in testing mode
# Add the root directory of the project to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# In all unit tests we are mocking the database functions to avoid actual DB initialization
class TestMainApp(unittest.TestCase):

# Apply the patch decorator to mock init_db
    @patch('app.db.init_db')
    def setUp(self, mock_init_db):
        # Mock the database initialization function
        self.mock_init_db = mock_init_db
        self.mock_init_db.return_value = None  # Ensure the mock doesn't do anything

        # Set up the Flask test client
        self.client = app.test_client()
        self.client.testing = True  # This enables better error handling in tests
        app.config['TESTING'] = True  # Enable testing mode
     
# @mock.patch decorator replaces the database connection to avoid actual DB calls
# (1) Mocking External Dependencies
# (2) Controlling the Return Values
# (3) Tracking Interactions
    @mock.patch('db.get_db_connection')
    @mock.patch('db.add_visit')
    
    def test_root(self, mock_add_visit, mock_get_db_connection):
        """Test the root endpoint."""
        # Mock the return value of add_visit
        mock_add_visit.return_value = {"id": 1, "timestamp": "2025-04-12T00:00:00", "ip": "127.0.0.1", "user_agent": "unknown"}
    
        # Now run the test to test the logic of the root endpoint
        response = self.client.get('/')
    
        # Assert that the response contains the formatted message
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome', response.data.decode())
        
# @mock.patch decorator replaces the database connection to avoid actual DB calls
    @mock.patch('db.get_db_connection')
    
    def test_hello_with_empty_name(self, mock_get_db_connection):
        """Test hello endpoint with empty name."""
        # Now run the test to test the logic of the hello endpoint
        response = self.client.get('/hello')
        
        # Assert that the response contains the formatted message
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello, mysterious visitor!", response.data)
    
    
# @mock.patch decorator replaces the database connection to avoid actual DB calls
    @mock.patch('db.get_db_connection')
    @mock.patch('db.add_visit')
    
    def test_visits_with_date_range(self, mock_add_visit, mock_get_db_connection):
        """Test visits endpoint with a date range."""
    
        # Mock the database connection to avoid actual DB calls
        mock_conn = mock.Mock()
        mock_get_db_connection.return_value = mock_conn
    
        # Mock the behavior of the database query or response
        # Mock methods on the mock_conn object if needed.
        mock_cursor = mock.Mock()
        mock_conn.cursor.return_value = mock_cursor
        # Mock methods on the mock_conn object if needed.
        mock_cursor.fetchall.return_value = [
            (1, "2022-01-01T00:00:00", "127.0.0.1", "Mozilla"),
            (2, "2022-12-31T00:00:00", "127.0.0.1", "Chrome")
            ]

        # Now run the test to test the logic of the visits endpoint
        response = self.client.get('/visits?from=2022-01-01&to=2023-01-01')
    
        # Assert the expected result
        self.assertEqual(response.status_code, 200)
        self.assertIn('2022-01-01', response.data.decode())  # Ensure visits are within the date range
        self.assertIn('2022-12-31', response.data.decode())  # Ensure visits are within the date range


# @mock.patch decorator replaces the database connection to avoid actual DB calls
    @mock.patch('db.get_db_connection')
    @mock.patch('db.add_visit')
    
    def test_visits_with_invalid_from_date(self, mock_add_visit ,mock_get_db_connection):
        """Test visits endpoint with an invalid 'from' date."""
    
        # Mock the database connection to avoid actual DB connection
        mock_get_db_connection.return_value = mock.MagicMock()
        
        # Now run the test to test the logic of the visits endpoint
        response = self.client.get('/visits?from=invalid-date')
        
        # Assert the expected result
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Invalid 'from' date format", response.data)  # Check for the error message
    
# @mock.patch decorator replaces the database connection to avoid actual DB calls
    @mock.patch('db.get_db_connection')

    def test_visit_not_found(self, mock_get_db_connection):
        """Test visit endpoint with a non-existing visit."""

        # Mock the db connection and cursor
        mock_conn = mock.Mock()
        mock_get_db_connection.return_value = mock_conn
        mock_cursor = mock.Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []  # Simulate no visits found for the visit

        # Now run the test to test the logic of the visit endpoint
        response = self.client.get('/visit/999')

        # Assert the expected result
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Visit not found", response.data)
    
# @mock.patch decorator replaces the database connection to avoid actual DB calls
    @mock.patch('db.get_db_connection')
    
    def test_hello_with_name(self, mock_get_db_connection):
        """Test hello endpoint with a name parameter."""
        
        # Now run the test to test the logic of the hello endpoint
        response = self.client.get('/hello?name=Mehdi')
        
        # Assert that the response contains the formatted message
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello, Mehdi!", response.data)

# @mock.patch decorator replaces the database connection to avoid actual DB calls
    @mock.patch('db.init_db')
    def test_db_initialization(self, mock_init_db):
        """Test DB initialization to ensure the mock is working."""

        # Now run the test to test the logic of the DB initialization
        self.mock_init_db()
        self.mock_init_db.assert_called_once()  # Ensure it was called once

# @mock.patch decorator replaces the database connection to avoid actual DB calls
    @mock.patch('db.get_db_connection')
    
    def test_hello_form(self, mock_get_db_connection):
        """Test the hello form."""
        
        # Now run the test to test the logic of the hello form
        response = self.client.get('/hello-form')
        
        # Assert that the response contains the form
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Say Hello', response.data)

#if __name__ == "__main__":
 #   unittest.main()
