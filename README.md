![made with python3](https://img.shields.io/badge/made%20with-python3-blue.svg) [![codecov](https://codecov.io/gh/BenjaminSimonis/Archivematica-API-Handler/branch/master/graph/badge.svg)](https://codecov.io/gh/BenjaminSimonis/Archivematica-API-Handler) 


# Archivematica-API-Handler 

A more easier API handler to make POST-Request and other calls with an ordinary body instead of an JSON body until the bug is fixed from Artefactual.
https://groups.google.com/forum/#!topic/archivematica/IvkI4xScFTU


## Requirements

- Python 3
- Archivematica with Standard Paths


## Installation

- Clone this project in /var/archivematica/
- cd Archivematica-API-Handler/
- sudo bash install.sh
- Edit credentials.py 
- Edit constants for own directory structure


## Behaviour pattern

- New SIPs will be ingested 24h after inserted in a source subdirectory. Just in case you haven't copied all the files yet.
- Finished Ingests are deleted from the Ingest server after a waiting period of 30 days (not Archive Server) to free up memory.


## Directory structure

- Python commands have to be executed in /var/archivematica/Archivematica-API-Handler/
- SIPs have to be stored in a sub directory like repo/ retro/ or ebooks/
  - For more or other ingest folder edit constants.py:26-35 and install.sh:13-15
```
/var/archivematica/
├── Archivematica-API-Handler
│   ├── apiHandler.py
│   ├── manualHandler.py
│   ├── constants.py
│   ├── credentials.py
│   ├── dbHandler.py
│   ├── help.py
│   ├── install.sh
│   ├── logger.py
│   ├── logs
│   ├── main.py
│   ├── processingConfs
│   ├── processingHandler.py
│   ├── README.md
│   ├── requirements.txt
│   ├── sourceHandler.py
│   └── storage.db
├── sharedDirectory
│   ├── sharedMicroServiceTasksConfigs
│   ├── ...
│   └── ...
└── source
    ├── done
    ├── ebooks
    ├── failed
    ├── repo
    └── retro
```

## Commands for automatic ingest

- Start automatic ingest\
```python3 main.py```

- Start automatic ingest in debug mode\
```python3 main.py DEBUG```


## Commands for manual ingest

- Print all commands with parameters\
```python3 manualHandler.py help```
  
- Start a new Transfer and approve it\
```python3 manualHandler.py start_transfer {'name for transfer'} {'type of transfer'} {'accession number'} {'foldername in source path'}``` 
  
- List all unapproved transfers\
```python3 manualHandler.py list_unapproved``` 
  
- Approve a specific transfer\
```python3 manualHandler.py approve_transfer {'type of transfer'} {'name for transfer'}```
  
- Get the status of an specific transfer by it's UUID\
```python3 manualHandler.py status_transfer {'uuid of transfer'}```
  
- Get a list of all completed transfers\
```python3 manualHandler.py completed_transfer```
  
- Hide a specific transfer by it's UUID\
```python3 manualHandler.py hide_transfer {'uuid of transfer'}```
  
- Get the status of a specific ingest by it's UUID\
```python3 manualHandler.py status_ingest {'uuid of ingest'}```
  
- Hide a specific ingest by it's UUID\
```python3 manualHandler.py hide_ingest {'uuid of ingest'}```

- List all ingests waiting for user input\
```python3 manualHandler.py waiting_ingests```

- List all completed ingests\
```python3 manualHandler.py completed_ingest```
