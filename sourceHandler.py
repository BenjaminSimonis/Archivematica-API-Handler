import json

from apiHandler import completed_ingests
from constants import AppConstants
from datetime import timedelta, datetime
from logger import write_log
from os import getcwd, listdir
from shutil import move, rmtree


# Check via API if an Ingest is completed
def is_ingest_complete(uuid):
    transfers = completed_ingests()
    write_log("sourceHandler.py:\t" + transfers, "[DEBUG]")
    j = json.dumps(transfers.text)
    write_log("sourceHandler.py:\t" + j, "[DEBUG]")
    results = j['results']
    write_log("sourceHandler.py:\t" + results, "[DEBUG]")
    if uuid in results:
        return True
    else:
        return False


# Move the source of an completed ingest to the done directory
def move_source_to_done(path, uuid):
    if is_ingest_complete(uuid):
        move(path, AppConstants.DONE_SOURCE_PATH)
        write_log("sourceHandler.py:\tMoved " + path + " to DONE Folder", "[INFO]")
        create_delete_date(path)
    else:
        write_log("sourceHandler.py:\tIngest " + uuid + " is not completed", "[DEBUG]")
    return


# Create a file with the name of the completed ingest folder with prefix "delete_" and a date in
# 30 days as suffix in timestamp format
def create_delete_date(path):
    delete_date = datetime.now() + timedelta(days=30)
    write_log("sourceHandler.py:\t" + delete_date, "[DEBUG]")
    delete_name = "delete_" + path + "_" + delete_date
    write_log("sourceHandler.py:\t" + delete_name, "[DEBUG]")
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
            write_log("sourceHandler.py:\t" + itemparts, "[DEBUG]")
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
        write_log("sourceHandler.py:\tDeleted " + path, "[INFO]")
        return True
    else:
        return False
