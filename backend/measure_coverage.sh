#!/bin/bash

coverage run --source=. --omit="*test_*" -m unittest discover -p "test_*" &&
    coverage report --fail-under=80 -m
