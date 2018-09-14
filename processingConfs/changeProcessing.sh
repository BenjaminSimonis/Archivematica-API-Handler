#!/usr/bin/env bash

rm -f /var/archivematica/sharedDirectory/sharedMicroServiceTasksConfigs/processingMCPConfigs/defaultProcessingMCP.xml
cp $1 /var/archivematica/sharedDirectory/sharedMicroServiceTasksConfigs/processingMCPConfigs/defaultProcessingMCP.xml
exit 0