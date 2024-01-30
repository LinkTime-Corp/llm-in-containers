# Tabular Data Analysis
## Oveview
This demo is designed to transform the way we interact with tabular data, particularly CSV files, using the advanced capabilities of Large Language Models and the LlamaIndex framework. 

Furthermore, we delve into the practical aspects of deploying Large Language Model applications using Docker. This process involves several key steps that ensure your LLM application is encapsulated within a Docker container, providing a consistent and isolated environment for operation, regardless of the underlying host system.

## Context
In this demo, we explore two innovative methods for querying tabular data, each with its unique approach and theoretical underpinnings. The first method, "mix self-consistency," originates from the paper ["Rethinking Tabular Data Understanding with Large Language Models"](https://arxiv.org/abs/2312.16702) by Liu et al., and offers a novel perspective on data interpretation through LLMs. The second method, "Chain of Tables" detailed in ["Chain-of-Table: Evolving Tables in the Reasoning Chain for Table Understanding"](https://arxiv.org/abs/2401.04398) by Wang et al., presents an advanced technique for evolving table-based data reasoning. 

Both methods are implemented using [Llama Packs](https://github.com/run-llama/llama-hub/tree/main/llama_hub/llama_packs/tables), a versatile and community-driven collection of prepackaged modules designed to enhance LLM applications.  

We've brought these approaches to life through an intuitive WebUI, resembling a chatbot interface, where users can interact with either ChatGPT or local models to execute their data queries. This setup not only showcases the practical applications of these theoretical approaches but also provides an accessible platform for users to experience the cutting-edge in tabular data querying.

## Prerequisites
Before diving into this demo, please ensure that your system meets the following prerequisites:
1. **Operating System**: The demo is compatible with Mac and Linux operating systems.

2. **Docker and wget**: It's required to have `docker`, `docker-compose` and `wget` installed on your system. Specifically, we have tested this demo with Docker Engine Community version 25.0.1. 

3. **OpenAI API Key for ChatGPT**: If you wish to use the ChatGPT functionality within this demo, an OpenAI API key is required. Please note that usage of this API is subject to OpenAI's pricing and usage policies.

## Quick Start
### Running the demo on CPU
1. Start by cloning this repo to your local machine:
```
git clone https://github.com/LinkTime-Corp/llm-in-containers.git
cd llm-in-containers/tabular-data-analysis
```
2. Insert your OpenAI API Key into conf/config.json for "OPENAI_API_KEY".
3. Download local model:
```
source download-models.sh
```
4. Launch the demo:
```
source run.sh
```
5. Visit the UI at http://localhost:8501. On the UI, you can choose either "ChatGPT" or "Local_LLM" (the local model you downloaded) to query the tabular data.
6. Shutdown the demo.
```
source shutdown.sh
```

### Running the demo on GPU
1. Start by cloning this repo to your local machine:
```
git clone https://github.com/LinkTime-Corp/llm-in-containers.git
cd llm-in-containers/tabular-data-analysis
```
2. Insert your OpenAI API Key into conf/config.json for "OPENAI_API_KEY". 
3. Launch the demo:
```
source run.sh -gpu
```
4. Visit the UI at http://localhost:8501. On the UI, you can choose either "ChatGPT" or "Local_LLM" (the default local model "mistral-openorca" is configured to run on GPU) to query the tabular data.
5. Shutdown the demo.
```
source shutdown.sh -gpu
```
