#!/bin/bash

pylint --fail-under=10.0 . && \
    flake8 .
