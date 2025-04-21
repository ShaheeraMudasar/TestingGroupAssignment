#!/bin/bash
echo "🔧 Starting integration test environment..."

# Build and start test containers in detached mode
docker-compose -f docker-compose-test.yml up -d --build

# Wait a few seconds to ensure services are up
sleep 5

# echo "🧪 Running integration tests..."
# docker-compose -f docker-compose-test.yml exec test_web pytest tests/test_integration.py

# Optional: shut down test containers after tests
# echo "🧹 Shutting down test containers..."
# docker-compose -f docker-compose-test.yml down

echo "✅ All done!"
