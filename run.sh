#!/usr/bin/bash
if [ ! -e logs ]; then
    mkdir logs
fi
python3 src/main.py

./clean_pycache.sh > /dev/null

