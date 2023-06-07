#!/bin/bash
if [ -e doc ]; then
    rm -rf doc
fi
mkdir doc
cd src
for mod in `find ecosystem_simulation | grep -v "__" | sed 's/\//./g' | sed  's/\.py$//g'`; do
    pydoc3 -w  $mod
done
mv *.html ../doc
cd ..
