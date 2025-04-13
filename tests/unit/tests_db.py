# TestCase: add_visit should save a visit's detail in database using mock data 
# and return with the visit info on homepage without errror
# 
import db
from db import get_db_connection, init_db, add_visit, get_all_visits, get_visit_by_id, format_visit_history
from datetime import datetime
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch
from main import visit

# 1. "get_db_connection":
# This function returns a database connection. 
# We’ll mock it in our tests to avoid hitting an actual database.

class TestDBFunctions(unittest.TestCase):

    # Test: get_db_connection should return a connection object (valid connection parameters)
    @patch("db.psycopg2.connect")
    def test_get_db_connection(self, mock_connect):
        # Given: Tvalid database connection parameters
        mock_connect.return_value = MagicMock()
        
        # When: get_db_connection is called
        conn = get_db_connection()

        # Then it should return a mock connection object      
        mock_connect.assert_called_once_with(
            dbname="test_db", 
            user="test_user", 
            password="test_password", 
            host="localhost", 
            port="5432"
        )
        self.assertIsInstance(conn, MagicMock)

# 2. "init_db()"
# This function interacts with the database to create a table.
# We’ll mock it to isolate it.

# Test: init_db should create the "visits" table if it doesn't exist (valid case)
    @patch("db.get_db_connection")
    def test_init_db(self, mock_get_conn):
        # Given: A mock database connection
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # When: init_db is called
        db.init_db()

        # Then: It should execute the SQL to create a table
        mock_cursor.assert_called_once_with('''
            CREATE TABLE IF NOT EXISTS visits (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                ip TEXT NOT NULL,
                user_agent TEXT NOT NULL
            )
        ''')

        mock_conn.commit.assert_called_once()

# 3. "add_visit()"
# This function inserts a visit into the database.
# We’ll mock the connection, cursor, and the database interaction.

# Test: add_visit should insert a new visit and return a visit object (valid input)
    @patch("db.get_db_connection")
    def test_add_visit(self, mock_get_conn):
        # Given: A mock database connection and cursor
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # Given: valid input: sample IP and User Agent
        #mock_cursor.fetchone.return_value = (1,)
        #mock_cursor.execute.return_value = None
        #mock_conn.commit.return_value = None
        #mock_cursor.return_value = mock_cursor  
        ip = "192.168.0.1"
        user_agent = "Mozilla/5.0"
        
        # When add_visit is called
        result = add_visit(ip, user_agent)
        
        # Then it should return a dictionary with visit details
        self.assertIn("id", result)
        self.assertIn("timestamp", result)
        self.assertEqual(result["ip"], ip)
        self.assertEqual(result["user_agent"], user_agent)
        
        # It should insert the visit into the database
        mock_cursor.execute.assert_called_once_with(
            'INSERT INTO visits (timestamp, ip, user_agent) VALUES (%s, %s, %s) RETURNING id',
            (result["timestamp"], ip, user_agent)
        )
        mock_conn.commit.assert_called_once()
    
# 4. "get_all_visits()"
# This function retrieves all visits.
# We'll mock the database interaction and test that it correctly returns a list.

    # Test: get_all_visits should return a list of visits (valid data from DB)
    @patch("psycopg2.connect")
    def test_get_all_visits(self, mock_connect):
        # Given a mocked connection and cursor with predefined rows
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        # Given mock rows from the database
        mock_cursor.fetchall.return_value = [
            (1, datetime(2023, 4, 12, 10, 0), "192.168.1.1", "Mozilla/5.0"),
            (2, datetime(2023, 4, 12, 11, 0), "192.168.1.2", "Chrome/91.0")
        ]
        
        # When get_all_visits is called
        visits = get_all_visits()
        
        # Then it should return a list of visit dictionaries
        self.assertEqual(len(visits), 2)
        self.assertEqual(visits[0]["id"], 1)
        self.assertEqual(visits[0]["ip"], "192.168.1.1")
        self.assertEqual(visits[1]["user_agent"], "Chrome/91.0")

# 5. "get_visit_by_id()"
# This function retrieves a visit by ID.
# We'll test it with a valid ID and a non-existent ID.

# Test: get_visit_by_id should return a visit by its ID (valid visit ID)
    @patch("psycopg2.connect")
    def test_get_visit_by_id(self, mock_connect):
        # Given a mocked connection and cursor with a predefined row
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        # Given a valid visit ID (1)
        mock_cursor.fetchone.return_value = (1, datetime(2023, 4, 12, 10, 0), "192.168.1.1", "Mozilla/5.0")
        
        # When get_visit_by_id is called with visit_id = 1
        visit = get_visit_by_id(1)
        
        # Then it should return the corresponding visit
        self.assertEqual(visit["id"], 1)
        self.assertEqual(visit["ip"], "192.168.1.1")

# Test: get_visit_by_id should return None if visit ID does not exist (invalid visit ID)
    @patch("psycopg2.connect")
    def test_get_visit_by_id_not_found(self, mock_connect):
        # Given a mocked connection and cursor with no results
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        # Given an invalid visit ID (9999) that does not exist
        mock_cursor.fetchone.return_value = None
        
        # When get_visit_by_id is called with visit_id = 9999
        visit = get_visit_by_id(9999)
        
        # Then it should return None
        self.assertIsNone(visit)


# 6. "format_visit_history()"
# This function formats the visit history.
# We’ll test it with an empty list and a populated list.

# Test: format_visit_history should return the same history (boundary test with empty list)
    def test_format_visit_history_empty(self):
        # Given an empty list of visit history
        history = []
        
        # When format_visit_history is called
        formatted_history = format_visit_history(history)
        
        # Then it should return the same empty list
        self.assertEqual(formatted_history, [])
    
    # Test: format_visit_history should return the same history (boundary test with non-empty list)
    def test_format_visit_history_non_empty(self):
        # Given a list of visit history
        history = [
            {"id": 1, "timestamp": datetime(2023, 4, 12, 10, 0), "ip": "192.168.1.1", "user_agent": "Mozilla/5.0"}
        ]
        
        # When format_visit_history is called
        formatted_history = format_visit_history(history)
        
        # Then it should return the same list of visits
        self.assertEqual(formatted_history, history)


#if __name__ == '__main__':
#    unittest.main()