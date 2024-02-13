# Setup environment on AWS
We suggest the following AWS EC2 instances as the environment to run the demo:
 * OS: Ubuntu 22.04 LTS
 * CPU instance: c5.2xlarge with 8 vCPUs and 16GB of RAM, $0.34 per hour as of 02/01/2024.
 * GPU instance: g5.xlarge with  NVIDIA A10G GPU, 4 vCPUs, and 16GB of RAM,  $1.006 per hour as of 02/01/2024.
  
By default, AWS EC2 creates a 'ubuntu' user and we run all the setup scripts under this user:
```
git clone https://github.com/LinkTime-Corp/llm-in-containers.git

cd llm-in-containers/env-setup/aws/ubuntu-22.04

bash docker-install.sh
```
To enable Docker commands for the 'ubuntu' user, please log out. For running this demo on GPU instances, proceed as follows:
```
bash nvidia-driver-install.sh
```
After the reboot is done, go back to the 'llm-in-containers/env-setup/aws/ubuntu-22.04' directory and run:
```
bash nvidia-container-install.sh

docker run -it --rm --gpus all ubuntu nvidia-smi
```
If everything is installed successfully, the final command will display Nvidia GPU and driver details.