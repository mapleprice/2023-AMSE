#!/bin/sh
python3 -m pip install requirements.txt

python3 unittest.py
python3 systemtest.py