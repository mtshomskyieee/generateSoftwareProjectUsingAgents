#!/bin/bash  

# Script to install dependencies, compile the project, and run unit tests for the Python Calculator application  

# Step 1: Install dependencies  
echo "Installing dependencies..."  
pip install -r requirements.txt  

# Step 2: Check if .py files need to be compiled (not applicable for Python but included for compatibility)  
# In Python, compilation is not necessary, so I'm skipping this step.  

# Step 3: Run unit tests  
echo "Running unit tests..."  
python -m unittest discover -s tests -p "*.py"  

echo "Script execution completed."  
exit 0