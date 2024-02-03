#!/bin/bash

source nvidia-container-runtime-script.sh

sudo apt-get install -y nvidia-container-runtime

sudo systemctl restart docker