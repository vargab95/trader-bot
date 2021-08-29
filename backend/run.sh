#!/bin/bash

MODE=$1
CONFIG_FILE=$2

if [[ -z $MODE || -z $CONFIG_FILE ]]
then
    echo "Usage is <mode> <config_file_path>"
    exit 1
fi

exec python3 ./main.py $MODE $CONFIG_FILE
