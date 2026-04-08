#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Run the Streamlit app
python -m streamlit run app.py
