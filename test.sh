#!/usr/bin/bash

python -m unittest tests/animal_tests.py

./clean_pycache.sh > /dev/null

