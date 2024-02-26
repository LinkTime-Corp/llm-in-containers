# Running PDF Parsers on Docker Containers
## Overview
This demo showcases running different PDF parsers on the same docker container. Three
approaches for parsing PDF files are included: [LlmSherpa](https://github.com/nlmatics/llmsherpa), [Unstructured](https://github.com/Unstructured-IO/unstructured), and [LlamaParse](https://github.com/run-llama/llama_parse).

## Prerequisites
Before diving into this demo, please ensure that your system meets the following prerequisites:
1. **Operating System**: The demo is compatible with Linux operating systems and tested on Ubuntu 22.04.

2. **Docker**: It's required to have `docker` installed on your system. Specifically, we have tested this demo with Docker Engine Community version 25.0.1 on Linux. 

3. **OpenAI API Key for ChatGPT**: If you wish to use the ChatGPT functionality within this demo, an OpenAI API key is required. Please note that usage of this API is subject to OpenAI's pricing and usage policies. We use OpenAI text generation models to optimize the parsing of some special components like titles or tables etc. Without this API key, you can still try all three approaches.
   
4. **LlamaParse API Key**: If you wish to try the newly launched LlamaParse API service, you need to get an API key from [here](https://cloud.llamaindex.ai/). As of today (02/26/2024), this API service is in preview mode for free. Without this API key, you will not be able to try LlamaParse.

## Quick Start
### Setup environment on AWS
Please follow this [README file](../env-setup/aws/ubuntu-22.04/README.md) to setup the demo environment on AWS EC2. Note that, GPU is not needed in this demo, so you can run it on any instance that is installed Docker.

### Running the demo
1. Start by cloning this repo to your instance with Docker installed:
```
git clone https://github.com/LinkTime-Corp/llm-in-containers.git
cd llm-in-containers/pdf2md
```
2. Replace 'your-openai-api-key' and 'your-llamaparse-api-key' with your API keys in the 'run.sh'. Then launch the demo. 
```
bash run.sh
```
3. Visit the UI at http://{IP of Host instance}:8501. On the UI, you can choose "LlamaParse", "LlmSherpa", or "Unstructured" to parse the uploaded PDF file.
4. Shut down the demo.
```
bash shutdown.sh
```