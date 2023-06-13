#!/bin/sh

echo "Installing Requirements..."
python3 -m pip install -r requirements.txt

echo "Running Unit Tests..."
python3 main/project/unittest.py

echo "Running System Test..."
python3 main/project/systemtest.py