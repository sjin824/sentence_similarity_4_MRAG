#!/bin/bash

# Create a virtual environment
python3.9 -m venv venv
source venv/bin/activate
git clone https://github.com/princeton-nlp/SimCSE.git
cd SimCSE
pip install .

# Go back
cd ..

# Install other dependencies
pip install -r requirements.txt

# Choose the model you want to use. Currently 1 model - simcse_api
# Run the API
python simcse_api.py

# Default port is 5000
echo "Simcse API is running on port 5000"