from db import get_visit_by_id, get_all_visits
from unittest.mock import patch, MagicMock
from hamcrest import assert_that, equal_to



# Unit tests for functions: add_visit (Tester: Mehdi)








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
