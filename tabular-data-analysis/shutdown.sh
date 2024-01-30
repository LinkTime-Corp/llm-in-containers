#!/bin/bash

echo "Shutting down app..."
if [ "$1" == "-gpu" ]; then
    docker-compose down
else
    docker-compose -f docker-compose-lit.yaml down
fi