#!/usr/bin/env bash

mkdir logs
sudo usermod -a -G archivematica $USER
cp ../sharedDirectory/sharedMicroServiceTasksConfigs/processingMCPConfigs/automatedProcessingMCP.xml processingConfs/
cp ../sharedDirectory/sharedMicroServiceTasksConfigs/processingMCPConfigs/defaultProcessingMCP.xml processingConfs/
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo pip3 install -r requirements.txt
sudo rm -f get-pip.py
mkdir ../source
mkdir ../source/ebooks
mkdir ../source/retro
mkdir ../source/repo
mkdir ../source/done
mkdir ../source/failed
