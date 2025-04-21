#!/bin/bash

echo "🔄 Starting full test workflow..."

cd ..

# 1. Run all unit tests
echo "🧪 Running unit tests..."
pytest tests/unit/test_html_utils.py
pytest tests/unit/test_rendering.py
pytest tests/unit/tests_db.py
pytest tests/unit/test_main.py

# 2. Run integration test setup and run the integration tests inside the container
echo "🔧 Running integration tests inside container..."
./tests/run-integration-tests.sh

# Shut down test containers after tests
echo "🧹 Shutting down test containers..."
docker-compose -f docker-compose-test.yml down

# 3. Run system (Playwright) tests from host
echo "🌐 Starting the web application for system tests"
./local-start.sh
echo "🌐 Running system tests (Playwright)..."
pytest --browser=chromium tests/system/test_system.py

# Shut down the app after tests
echo "🧹 Shutting down the app..."
docker compose down

echo "✅ All tests completed!"