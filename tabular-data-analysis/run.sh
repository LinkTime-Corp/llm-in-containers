#!/bin/bash

CONFIG_FILE="conf/config.json"

if [ "$1" == "-gpu" ]; then
    echo "GPU option provided. Running on GPU..."
    # Set CPU_Only to false
    sed -i'' -e 's/"CPU_Only": true/"CPU_Only": false/' "$CONFIG_FILE"
    docker build -t tabular-data-analysis:1.0 .
    docker-compose up -d
else
    echo "Running on CPU by default..."
    # Set CPU_Only to true
    sed -i'' -e 's/"CPU_Only": false/"CPU_Only": true/' "$CONFIG_FILE"
    docker build -f Dockerfile.lit -t tabular-data-analysis:lit-1.0 .
    docker-compose -f docker-compose-lit.yaml up -d
fi