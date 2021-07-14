#!/bin/bash

safety check -r requirements.txt && \
    bandit -r .
