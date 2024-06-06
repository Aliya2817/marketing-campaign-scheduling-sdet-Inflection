#!/bin/bash

# Print message for creating a virtual environment
echo "Creating a virtual environment..."
python3 -m venv venv

# Check if the virtual environment was created successfully
if [ -d "venv" ]; then
    echo "Virtual environment created successfully."
else
    echo "Failed to create virtual environment."
    exit 1
fi

# Print message for activating the virtual environment
echo "Activating the virtual environment..."
source venv/bin/activate

# Check if the virtual environment was activated successfully
if [ $? -eq 0 ]; then
    echo "Virtual environment activated successfully."
else
    echo "Failed to activate virtual environment."
    exit 1
fi

# Print message for installing dependencies
echo "Installing dependencies from requirements.txt..."
pip3 install -r requirements.txt

# Check if dependencies were installed successfully
if [ $? -eq 0 ]; then
    echo "Dependencies installed successfully."
else
    echo "Failed to install dependencies."
    exit 1
fi

# Print message for executing the test cases
echo "Executing the test cases..."
pytest --disable-warnings --html=report.html test/test_*.py

# Check if the test cases were executed successfully
if [ $? -eq 0 ]; then
    echo "Test cases executed successfully. Report generated, check report.html"
else
    echo "Failed to execute test cases."
    exit 1
fi
