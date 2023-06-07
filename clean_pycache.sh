#!/bin/bash
for file in `find src | grep '__pycache__'`; do
    rm -rf $file
    echo "$file removed"
done

