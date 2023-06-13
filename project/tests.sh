#!/bin/sh

echo "Installing Requirements..."
python3 -m pip install requirements.txt

echo "Running Unit Tests..."
python3 unittest.py

echo "Running System Test..."
python3 systemtest.py