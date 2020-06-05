#!/bin/bash

python3 -m coverage run --source=. --omit="*test_*.py","*tools/*" -m unittest
python3 -m coverage report -m

python3 -m pylint --reports=y --rcfile .pylintrc `find . -type f -name "*.py" -printf "%P\n" | grep -v ".vscode"`

echo; echo
git grep TODO

echo; echo
git grep FIXME
