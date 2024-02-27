#!/bin/bash
set -e -u

docker build -t pdf2md:1.0 .
docker-compose up -d
