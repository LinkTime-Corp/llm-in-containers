#!/bin/bash
set -e -u

CUR_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
CONFIG_FILE="${CUR_PATH}/conf/config.json"

find_settings() {
    local file_path="$1"
    local found=0

    while IFS= read -r line; do
        if [[ "$line" == *'"database":'* ]]; then
            found=1
        fi
        if [[ $found -eq 1 && "$line" == *'"password":'* ]]; then
            PASSWORD=$(echo "$line" | sed -e 's/.*"password": *"\(.*\)".*/\1/')
        fi
        if [[ "$line" == *'"type": "CPU_Only"'* ]]; then
            found=2
        fi
        if [[ $found -eq 2 && "$line" == *'"name":'* ]]; then
            CPU_LLM=$(echo "$line" | sed -e 's/.*"name": *"\(.*\)".*/\1/')
        fi
        if [[ "$line" == *'"type": "GPU_Enabled"'* ]]; then
            found=3
        fi
        if [[ $found -eq 3 && "$line" == *'"name":'* ]]; then
            GPU_LLM=$(echo "$line" | sed -e 's/.*"name": *"\(.*\)".*/\1/')
        fi
    done < "$file_path"
}

find_settings "$CONFIG_FILE"

if [ $# -eq 0 ]; then
    echo "Running on CPU by default..."
    sed -i'' -e "s/MYSQL_ROOT_PASSWORD:.*/MYSQL_ROOT_PASSWORD: \"$PASSWORD\"/" docker-compose-lit.yaml

    # Set CPU_Only to true
    sed -i'' -e 's/"CPU_Only": false/"CPU_Only": true/' "$CONFIG_FILE"
    docker build -f Dockerfile.lit -t text2sql:lit-1.0 .
    docker-compose -f docker-compose-lit.yaml up -d
    echo "waiting for containers to start..."
    sleep 5
    docker exec text2sql_ollama_1 sh -c "ollama run $CPU_LLM --verbose"
else
    if [ "$1" == "-gpu" ]; then
        echo "GPU option provided. Running on GPU..."
        sed -i'' -e "s/MYSQL_ROOT_PASSWORD:.*/MYSQL_ROOT_PASSWORD: $PASSWORD/" docker-compose.yaml

        # Set CPU_Only to false
        sed -i'' -e 's/"CPU_Only": true/"CPU_Only": false/' "$CONFIG_FILE"
        docker build -t text2sql:1.0 .
        docker-compose up -d
        echo "waiting for containers to start..."
        sleep 5
        docker exec text2sql_ollama_1 sh -c "ollama run $GPU_LLM --verbose"
    fi
fi
docker ps -a | grep text2sql
