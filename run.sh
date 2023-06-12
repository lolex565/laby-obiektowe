#!/bin/bash
if [ ! -e logs ]; then
    mkdir logs
fi
if [ ! -e graphs ]; then
    mkdir graphs
fi
if [ ! -e csv ]; then
    mkdir csv
fi
python3 src/main.py

./clean_pycache.sh > /dev/null

