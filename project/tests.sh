#!/bin/sh
cd main/project/

echo "===================================="
echo "Installing Requirements..."
echo "===================================="

python3 -m pip install -r requirements.txt

echo "===================================="
echo "Running Unit Tests..."
echo "===================================="

python3 unittests.py

echo "===================================="
echo "Running System Test..."
echo "===================================="

python3 systemtests.py