#!/usr/bin/env bash

sudo chmod 757 -R sharedDirectory/sharedMicroServiceTasksConfigs/processingMCPConfigs/
cp ../sharedDirectory/sharedMicroServiceTasksConfigs/processingMCPConfigs/automatedProcessingMCP.xml processingConfs/
cp ../sharedDirectory/sharedMicroServiceTasksConfigs/processingMCPConfigs/defaultProcessingMCP.xml processingConfs/
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo python3 -m pip install requests
sudo rm get-pip.py
mkdir ../source
mkdir ../source/ebooks
mkdir ../source/retro
mkdir ../source/freidok
mkdir ../source/done
