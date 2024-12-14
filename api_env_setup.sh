#!/bin/bash

# 1. Create a virtual environment
python3.9 -m venv venv
source venv/bin/activate

# 2. Install the required packages - simcse
git clone https://github.com/princeton-nlp/SimCSE.git
cd SimCSE
pip install .

# 3. The scikit-learn should be update actually
pip uninstall scikit-learn -y
pip install scikit-learn==0.24.2

# 4. Go back. Install the other required packages. Optional: Remove the SimCSE folder
cd ..
pip install -r requirements.txt
# rm -rf SimCSE

# 5. Run the API
python simcse_api.py
