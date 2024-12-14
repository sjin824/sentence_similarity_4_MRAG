#!/bin/bash

# 1. Create a virtual environment
python3.9 -m venv venv
source venv/bin/activate

# 2. Install the required packages - simcse
git clone https://github.com/princeton-nlp/SimCSE.git
cd SimCSE
pip install .

# 3. Install the other required packages 
pip install -r requirements.txt

# 4. The scikit-learn should be update actually
pip uninstall scikit-learn -y
pip install scikit-learn==0.24.2

# 5. Go back. Optional: Remove the SimCSE folder
cd ..
# rm -rf SimCSE

# 6. Run the API
python simcse_api.py

# 7. Test the API
python test_api.py