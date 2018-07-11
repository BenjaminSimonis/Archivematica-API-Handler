# Archivematica-API-Handler

A more easier API handler to make POST-Request and other calls with an ordinary body instead of an JSON body until the bug is fixed from Artefactual.
https://groups.google.com/forum/#!topic/archivematica/IvkI4xScFTU

##Requirements

- Python 3
- Archivematica with Standard Paths


##Installation

- clone this project in /var/archivematica/
- sudo bash install.sh


##Commands

- python3 apiHandler.py help 
  - Print all commands with parameters
  
- python3 apiHandler.py start_transfer {'name for transfer'} {'type of transfer'} {'accession number'} {'foldername in source path'} 
  - Start a new Transfer and approve it
  
- python3 apiHandler.py list_unapproved 
  - List all unapproved transfers
  
- python3 apiHandler.py approve_transfer {'type of transfer'} {'name for transfer'}
  - Approve a specific transfer
  
- python3 apiHandler.py apiHandler.py status_transfer {'uuid of transfer'}
  - Get the status of an specific transfer by it's UUID
  
- python3 apiHandler.py apiHandler.py completed_transfer
  - Get a list of all completed transfers
  
- python3 apiHandler.py apiHandler.py hide_transfer {'uuid of transfer'}
  - Hide a specific transfer by it's UUID
  
- python3 apiHandler.py apiHandler.py status_ingest {'uuid of ingest'}
  - Get the status of a specific ingest by it's UUID
  
- python3 apiHandler.py apiHandler.py hide_ingest {'uuid of ingest'}
  - Hide a specific ingest by it's UUID

- python3 apiHandler.py apiHandler.py waiting_ingests
  - List all ingests waiting for user input

- python3 apiHandler.py apiHandler.py completed_ingest
  - List all completed ingests