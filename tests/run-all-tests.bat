@echo off
echo 🔄 Starting full test workflow...

:: Go back to home directory where docker-compose files exist
cd .. 

:: 1. Run all unit tests
echo 🧪 Running unit tests...
pytest tests/unit/test_html_utils.py
pytest tests/unit/test_rendering.py
pytest tests/unit/tests_db.py
pytest tests/unit/test_main.py

:: 2. Run integration test setup and run the integration tests inside the container
echo 🔧 Running integration tests inside container...
call tests/run-integration-tests.bat

:: Shut down test containers after tests
echo 🧹 Shutting down test containers...
docker-compose -f docker-compose-test.yml down 

:: 3. Run system (Playwright) tests from host
echo Starting the web application for system tests
call local-start.bat
echo 🌐 Running system tests (Playwright)...
pytest --browser=chromium tests/system/test_system.py

# Shut down the app after tests
echo "🧹 Shutting down the app..."
docker compose down

echo ✅ All tests completed!
pause
