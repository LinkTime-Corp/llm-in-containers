#!/bin/bash

CONFIG_FILE="conf/config.json"

find_model_info() {
    local file_path="$1"
    local found=0

    while IFS= read -r line; do
        if [[ "$line" == *'"type": "GPU_Enabled"'* ]]; then
            found=1
        fi
        if [[ $found -eq 1 && "$line" == *'"name":'* ]]; then
            GPU_MODEL_NAME=$(echo "$line" | sed -e 's/.*"name": *"\(.*\)".*/\1/')
            break
        fi
    done < "$file_path"
}

find_model_info "$CONFIG_FILE"

if [ "$1" == "-gpu" ]; then
    echo "GPU option provided. Running on GPU..."
    sed -i'' -e "s/command:.*/command: $GPU_MODEL_NAME/" docker-compose.yaml

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