#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "-----------------------------------"
echo "Activating virtual environment..."
echo "-----------------------------------"

# Adjust this path if your venv folder has a different name
source venv/bin/activate

echo "-----------------------------------"
echo "Running test suite..."
echo "-----------------------------------"

# Run pytest
pytest

TEST_RESULT=$?

echo "-----------------------------------"

if [ $TEST_RESULT -eq 0 ]; then
    echo "All tests passed ✅"
    exit 0
else
    echo "Tests failed ❌"
    exit 1
fi
