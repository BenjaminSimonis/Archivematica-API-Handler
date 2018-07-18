import json

from apiHandler import completed_transfers
from datetime import timedelta, datetime
from os import getcwd, listdir
from shutil import move, rmtree
from sysParameters import DONE_SOURCE_PATH


# Check via API if an Ingest is completed
def is_ingest_complete(uuid):
    transfers = completed_transfers()
    j = json.dumps(transfers.text)
    results = j['results']
    if uuid in results:
        return True
    else:
        return False


# Move the source of an completed ingest to the done directory
def move_source_to_done(path):
    move(path, DONE_SOURCE_PATH)
    create_delete_date(path)
    return


# Create a file with the name of the completed ingest folder with prefix "delete_" and a date in
# 30 days as suffix in timestamp format
def create_delete_date(path):
    delete_date = datetime.now() + timedelta(days=30)
    delete_name = "delete_" + path + "_" + delete_date
    f = open(delete_name, "w+")
    f.close()
    return


# Check the current timestamp is greater than the timestamp in the delete file
# return true if file is deletable otherwise return false
def check_delete_date(path):
    cwd = getcwd()
    list = listdir(cwd)
    for item in list:
        if item.startswith("delete"):
            itemparts = item.split("_")
            if itemparts[1] == path and itemparts[2] < datetime.now():
                return True
            elif itemparts[1] == path:
                return False
            else:
                continue
    return False


# Delete a source folder from the done directory after checking the delete date
def delete_ingested_source(path):
    if check_delete_date(path):
        rmtree(path)
        return True
    else:
        return False
