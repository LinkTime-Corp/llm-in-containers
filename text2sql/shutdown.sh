#!/bin/bash
set -e -u

echo "Shutting down app..."
if [ $# -eq 0 ]; then
    docker-compose -f docker-compose-lit.yaml down
else
    if [ "$1" == "-gpu" ]; then
        docker-compose down
    fi
fi
set +e +u
