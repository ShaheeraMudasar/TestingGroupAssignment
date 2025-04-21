✅ **How to Run All Tests Automatically**
All tests (unit, integration, and system) can be executed using the provided automation scripts.

🪟 **For Windows users**
Run:
``` sh 
   run-all-tests.bat
```
🍎 **For MacOS / Linux users**
Run:
```sh 
   ./run-all-tests.sh
```
🧪 **What the script does:**
1. Runs all unit tests 
2. Builds and starts the integration test container
3. Runs integration tests inside Docker
4. Shuts down the integration container
5. Starts the main application
6. Runs system tests (Playwright)