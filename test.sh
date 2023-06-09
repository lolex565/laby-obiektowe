#!/bin/bash

python3 -m unittest tests/animal_tests.py

./clean_pycache.sh > /dev/null

