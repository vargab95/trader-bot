#!/bin/bash

APPLICATION_TYPE=$1
if [[ -z $APPLICATION_TYPE ]]
then
    APPLICATION_TYPE=$TRADER_APPLICATION_TYPE
fi

CONFIG_FILE=$2
if [[ -z $CONFIG_FILE ]]
then
    CONFIG_FILE=$TRADER_CONFIG_FILE
fi

if [[ -z $APPLICATION_TYPE || -z $CONFIG_FILE ]]
then
    echo "Usage is <mode> <config_file_path> or set via TRADER_APPLICATION_TYPE and TRADER_CONFIG_FILE environment variables"
    exit 1
fi

exec python3 ./main.py $APPLICATION_TYPE $CONFIG_FILE
