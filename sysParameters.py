# Archivematica informations
TS_LOCATION_UUID = "UUID"
AUTH_HEADER = {"Authorization": "ApiKey test:test"}


# API informations
URL = "URL_ADDRESS"
URL_API = "/api"
URL_TRANSFER = URL_API + "/transfer"
URL_INGEST = URL_API + "/ingest"


# General path informations
WORKING_PATH = "/var/archivematica"
HANDLER_PATH = WORKING_PATH + "/Archivematica-API-Handler/"
SOURCE_PATH = WORKING_PATH + "/source"
EBOOK_SOURCE_PATH = SOURCE_PATH + "/ebooks"
RETRO_SOURCE_PATH = SOURCE_PATH + "/retro"
FREIDOK_SOURCE_PATH = SOURCE_PATH + "/freidok"
DONE_SOURCE_PATH = SOURCE_PATH + "/done"


# Processing path informations
PROCESS_PATH = WORKING_PATH + "/sharedDirectory/sharedMicroServiceTasksConfigs/processingMCPConfigs/"
PROCESS_DEFAULT = "defaultProcessingMCP.xml"
PROCESS_AUTOMATED = "automatedProcessingMCP.xml"
PROCESS_PATH_AUTOMATED = PROCESS_PATH + PROCESS_AUTOMATED
PROCESS_PATH_DEFAULT = PROCESS_PATH + PROCESS_DEFAULT
LOCAL_PROCESS_DIR = "processingConfs/"
