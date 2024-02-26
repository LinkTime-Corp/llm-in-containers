#!/bin/bash
set -e -u

docker build -t pdf2md:1.0 .
docker run -d -p 8501:8501 \
 -e OPENAI_API_KEY='your-openai-api-key' \
 -e LLAMAPARSE_API_KEY= 'your-llamaparse-api-key'\
 --name pdf2md \
  pdf2md:1.0
