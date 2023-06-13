#!/bin/sh
cd main/project/

echo "Installing Requirements..."
python3 -m pip install -r requirements.txt

echo "Running Unit Tests..."
python3 unittest.py

echo "Running System Test..."
python3 systemtest.py