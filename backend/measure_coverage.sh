#!/bin/bash

python3 -m coverage run --source=. --omit="*test_*,./tools*" -m unittest discover -p "test_*" &&
    python3 -m coverage report --fail-under=80 -m | grep -vE "(100%)$"
