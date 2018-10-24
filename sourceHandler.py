import json
import subprocess
from os.path import isdir

from apiHandler import completed_ingests
from constants import AppConstants
from datetime import timedelta, datetime
from dbHandler import db_handler
from logger import write_log
from os import listdir, remove
from shutil import move, rmtree

AppConstants = AppConstants()


######################################
## Methods for old finished Ingests ##
######################################

# TODO: Make two entrance points for calling from other methods.
# One for moving Finished Ingests to done / delete
# Second one to check, if delete date has arrived and delete old stuff from drive and DB!

# Private method
# Check via API if an Ingest is completed
def is_ingest_complete(uuid):
    transfers = completed_ingests()
    write_log("sourceHandler.py:\t" + str(transfers), "[DEBUG]")
    j = json.loads(transfers.text)
    write_log("sourceHandler.py:\t" + str(j), "[DEBUG]")
    results = j['results']
    write_log("sourceHandler.py:\t" + str(results), "[DEBUG]")
    if uuid in results:
        return True
    else:
        return False


# Private method
# Check the current timestamp is greater than the timestamp in the delete file
# return true if file is deletable otherwise return false
def check_delete_dates(path, done_dir):
    for item in done_dir:
        if item.startswith("delete"):
            itemparts = item.split("_")
            if itemparts[1] in path:
                write_log("sourceHandler.py:\t" + str(itemparts), "[DEBUG]")
                now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                if datetime.strptime(itemparts[2], '%Y-%m-%d %H:%M:%S') < datetime.strptime(now, '%Y-%m-%d %H:%M:%S'):
                    remove(str(AppConstants.DONE_SOURCE_PATH) + "/" + str(item))
                    return True
                else:
                    return False
            else:
                continue


# Public method
# Delete a source folder from the done directory after checking the delete date
def delete_ingested_source():
    done_dir = listdir(str(AppConstants.DONE_SOURCE_PATH))
    for d_dir in done_dir:
        path = str(AppConstants.DONE_SOURCE_PATH) + "/" + str(d_dir)
        if isdir(path):
            if check_delete_dates(path, done_dir):
                rmtree(path)
                db_handler(AppConstants.CLEANING, None, d_dir)
                write_log("sourceHandler.py:\tDeleted " + str(path), "[DELETE]")


######################################
## Methods for new finished Ingests ##
######################################

# Public method
# Move the source of an completed ingest to the done directory
def move_source_to_done(path, uuid):
    if is_ingest_complete(uuid):
        move(path, str(AppConstants.DONE_SOURCE_PATH))
        write_log("sourceHandler.py:\tMoved " + str(path) + " to DONE Folder", "[INFO]")
        create_delete_date(path, uuid)
    else:
        write_log("sourceHandler.py:\tIngest " + str(uuid) + " is not completed", "[DEBUG]")
    return


# Private method
# Create a file with the name of the completed ingest folder with prefix "delete_" and a date in
# 30 days as suffix in timestamp format
def create_delete_date(path, uuid):
    delete_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    db_handler(AppConstants.TRANSFER, AppConstants.UPDATE_DELETE_DATE, delete_date, uuid)
    write_log("sourceHandler.py:\t" + str(delete_date), "[DEBUG]")
    delete_name = "delete_" + str(path).split("/")[-1] + "_" + str(delete_date)
    write_log("sourceHandler.py:\t" + str(delete_name), "[DEBUG]")
    subprocess.call(['touch', (str(AppConstants.DONE_SOURCE_PATH) + "/" + delete_name)])
    return
