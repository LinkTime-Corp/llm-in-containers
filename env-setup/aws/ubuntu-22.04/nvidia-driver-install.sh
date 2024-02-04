#!/bin/bash
set -e -u

sudo apt-get update

sudo apt install -y ubuntu-drivers-common

ubuntu-drivers devices

sudo ubuntu-drivers autoinstall

sudo reboot