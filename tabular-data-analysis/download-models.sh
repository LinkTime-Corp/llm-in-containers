#!/bin/bash
set -e -u

CONFIG_FILE="conf/config.json"

find_model_info() {
    local file_path="$1"
    local found=0

    while IFS= read -r line; do
        if [[ "$line" == *'"type": "CPU_Only"'* ]]; then
            found=1
        fi
        if [[ $found -eq 1 && "$line" == *'"url":'* ]]; then
            CPU_MODEL_URL=$(echo "$line" | sed -e 's/.*"url": *"\(.*\)".*/\1/')
            break
        fi
    done < "$file_path"
}

find_model_info "$CONFIG_FILE"

mkdir -p models
wget ${CPU_MODEL_URL} -P models/
