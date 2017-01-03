#!/bin/bash
# Filters out unneeded deps from libraries.txt.lock be examining libraries.txt
#  Appends libraries-vcs.txt, then replaces libraries.txt.lock
filter=$(cat libraries.txt | cut -d= -f 1 | xargs | sed -e 's/ /\\|/g')
grep $filter libraries.txt.lock > temp.txt
cat libraries-vcs.txt >> temp.txt
mv temp.txt libraries.txt.lock
# Remove patch version; always accept security-related fixes
sed -i 's/==/~=/' ./libraries.txt.lock
