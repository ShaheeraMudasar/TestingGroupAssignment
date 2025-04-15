from db import get_visit_by_id, get_all_visits, add_visit
from unittest.mock import patch, MagicMock
from hamcrest import assert_that, equal_to
from datetime import datetime


# Unit tests for functions: add_visit (Tester: Mehdi)

@patch("db.psycopg2.connect")
def test_add_visit_returns_data(mock_connect):
    # Given: Mock the DB connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Mock the current timestamp and the DB response
    mock_timestamp = datetime.now()
    mock_cursor.fetchone.return_value = (1,)  # The inserted visit ID

    # When: Call the function with test data
    ip = "127.0.0.1"
    user_agent = "TestAgent"
    result = add_visit(ip, user_agent)

    # THEN: Assert the result is as expected
    expected = {
        "id": 1,
        "timestamp": mock_timestamp,
        "ip": ip,
        "user_agent": user_agent
    }

    # Assert the result is as expected
    assert_that(result["id"], equal_to(1))
    assert_that(result["ip"], equal_to(ip))
    assert_that(result["user_agent"], equal_to(user_agent))

# Test: add_visit should handle exceptions (e.g., database connection failure)
@patch("db.psycopg2.connect")
def test_add_visit_handles_db_exception(mock_connect):
    # Given: Simulate a database connection error
    mock_connect.side_effect = Exception("Database connection error")

    # When: Call the function and check if it raises the correct exception
    try:
        add_visit("127.0.0.1", "TestAgent")
    # The: Assert the exception is raised
    except Exception as e:
        assert_that(str(e), equal_to("Database connection error"))


# Unit tests for functions: get_all_visits (Tester: Detelina)

@patch("db.psycopg2.connect")
def test_get_all_visits_returns_data(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "2025-01-01 12:00:00", "127.0.0.1", "Mozilla")
    ]

    result = get_all_visits()

    assert result == [
        {"id": 1, "timestamp": "2025-01-01 12:00:00", "ip": "127.0.0.1", "user_agent": "Mozilla"}
    ]

@patch("db.psycopg2.connect")
def test_get_all_visits_returns_empty(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = []

    result = get_all_visits()

    assert result == []











# Unit tests for functions: get_visit_by_id (Tester: Shaheera)


# Test: get_visit_by_id should return visit dict when ID exists
@patch("db.psycopg2.connect")
def test_get_visit_by_id_returns_data(mock_connect):
    # Mock the DB connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Mock the DB response
    mock_cursor.fetchone.return_value = (1, "2025-01-01 00:00:00", "127.0.0.1", "TestAgent")

    result = get_visit_by_id(1)
    expected = {
        "id": 1,
        "timestamp": "2025-01-01 00:00:00",
        "ip": "127.0.0.1",
        "user_agent": "TestAgent"
    }
    assert_that(result, equal_to(expected))

# Test: get_visit_by_id should return None when ID does not exist
@patch("db.psycopg2.connect")
def test_get_visit_by_id_returns_none(mock_connect):
    # Mock the DB connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Mock the DB response to return None
    mock_cursor.fetchone.return_value = None

    result = get_visit_by_id(999)
    assert_that(result, equal_to(None))
