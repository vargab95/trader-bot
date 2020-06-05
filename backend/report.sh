#!/bin/bash

python3 -m coverage run --source=. --omit="*ut_*.py" -m unittest `find . -type f -name "ut_*.py" -printf "%P\n"`
python3 -m coverage report -m

python3 -m pylint --reports=y --rcfile .pylintrc `find . -type f -name "*.py" -printf "%P\n" | grep -v ".vscode"`

echo; echo
git grep TODO

echo; echo
git grep FIXME
