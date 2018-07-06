#!/usr/bin/env python
import base64
import json
import requests
import sys

from os import fsencode
from time import sleep

from help import *
from sysParameters import *

######################################
########### Transfer API #############
######################################


# URL: /api/transfer/start_transfer/
# Verb: POST
# Start a transfer
# Parameters: JSON body
# Response: JSON
def start_transfer(name, type, accession, path):
    url = URL_TRANSFER + "/start_transfer/"
    print("Starting Transfer")
    dataset = {"name": name, "type": type, "accession": accession, "paths[]": [create_base64_path(path)],
               "row_ids[]": [""]}
    return start_and_approve(post_request(url, dataset))


# URL: /api/transfer/unapproved
# Verb: GET
# Returns a list of transfers waiting for approval.
# Response: JSON
def list_unapproved_transfers():
    url = URL_TRANSFER + "/unapproved"
    print("Unapproved Transfers")
    return get_request(url)


# URL: /api/transfer/approve
# Verb: POST
# Approve a transfer waiting to be started.
# Parameters: JSON body
# Response: JSON
def approve_transfer(type, dir):
    url = URL_TRANSFER + "/approve"
    print("Approve Transfer")
    dataset = {"type": type, "directory": dir}
    return post_request(url, dataset)


# URL: /api/transfer/status/<transfer UUID>/
# Verb: GET
# Returns the status of the transfer.
# Response: JSON
def status_transfer(uuid):
    url = URL_TRANSFER + "/status/" + uuid
    print("Status Transfer: " + uuid)
    get_request(url)
    return


# URL: /api/transfer/<transfer UUID>/delete/
# Verb: DELETE
# Hide a transfer
# Response: JSON
def hide_transfer(uuid):
    url = URL_TRANSFER + "/" + uuid + "/delete/"
    print("Hide Transfer: " + uuid)
    delete_request(url)
    pass


# URL: /api/transfer/completed/
# Verb: GET
# Return list of Transfers that are completed
# Response: JSON
def completed_transfers():
    url = URL_TRANSFER + "/completed/"
    print("Completed Transfers")
    get_request(url)
    return


######################################
############ Ingest API ##############
######################################


# URL: /ingest/status/<unit UUID>/
# Verb: GET
# Returns the status of the SIP
# Response: JSON
def status_ingest(uuid):
    url = URL_INGEST + "/status/" + uuid + "/"
    print("Status Ingest: " + uuid)
    get_request(url)
    return


# URL: /api/ingest/<SIP UUID>/delete/
# Verb: DELETE
# Hide a SIP
# Response: JSON
def hide_ingest(uuid):
    url = URL_INGEST + "/" + uuid + "/delete/"
    print("Hide Ingest: " + uuid)
    delete_request(url)
    return


# URL: /api/ingest/waiting
# Verb: GET
# Returns a list of SIPs waiting for user input.
# Response: JSON
def waiting_for_user_ingests():
    url = URL_INGEST + "/waiting"
    print("Ingests waiting for user input")
    get_request(url)
    return


# URL: /api/ingest/completed/
# Verb: GET
# Return list of SIPs that are completed
# Response: JSON
def completed_ingests():
    url = URL_INGEST + "/completed/"
    print("Completed Ingests")
    get_request(url)
    return


# URL: /api/transfer/reingest
# Verb: POST
# Start a full reingest.
# Parameters: JSON body
# Response: JSON
def start_full_reingest(name, uuid):
    url = URL_TRANSFER + "/reingest"
    print("Full Re-Ingest")
    dataset = {"name": name, "uuid": uuid}
    post_request(url, dataset)
    pass


# URL: /api/ingest/reingest
# Verb: POST
# Start a partial or metadata-only reingest.
# Parameters: JSON body
# Response: JSON
def start_partial_reingest(name, uuid):
    url = URL_INGEST + "/reingest"
    print("Full Re-Ingest")
    dataset = {"name": name, "uuid": uuid}
    post_request(url, dataset)
    return


# URL: /api/ingest/copy_metadata_files/
# Verb: POST
# Add metadata files to a SIP.
# Parameters: JSON body
# Response: JSON
def adding_md_to_ingest():
    pass


######################################
####### Archivematica Caller #########
######################################


def get_request(path):
    r = requests.get((URL + path), headers=AUTH_HEADER)
    process_response(r)
    return r


def post_request(path, dataset):
    r = requests.post((URL + path), data=dataset, headers=AUTH_HEADER)
    process_response(r)
    return r


def delete_request(path):
    r = requests.delete((URL + path), headers=AUTH_HEADER)
    process_response(r)
    return r


######################################
####### Preprocessing Calls ##########
######################################


def create_base64_path(target_path):
    if target_path == "":
        path = TARGET_SOURCE
    else:
        path = target_path
    base_path = base64.b64encode(fsencode(TS_LOCATION_UUID) + b':' + fsencode(path))
    return base_path


######################################
######### Processing Calls ###########
######################################

def start_and_approve(r):
    raw_json_start = json.loads(r.text)
    start_dir_name = raw_json_start["path"].split("/")[-2]
    sleep(5)
    unapproved_transfers = json.loads(list_unapproved_transfers().text)
    for result in unapproved_transfers["results"]:
        if result["directory"] == start_dir_name:
            approve_transfer(result["type"], start_dir_name)
            break
        else:
            continue
    return


######################################
####### Postprocessing Calls #########
######################################

def process_response(r):
    if r.status_code == 200:
        print("Success!")
        print(r.text)
    else:
        print("Failed!")
        raise Exception(r.reason)
    return


######################################
########### Initializing #############
######################################

def init():
    method = sys.argv[1]
    if method == "help":
        if sys.argv.__len__() == 2:
            list_commands()
            return
        else:
            command_description(sys.argv[2])
            return
    elif method == "start_transfer" and sys.argv.__len__() == 6:
        start_transfer(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        return
    elif method == "list_unapproved":
        list_unapproved_transfers()
        return
    elif method == "approve_transfer" and sys.argv.__len__() == 4:
        approve_transfer(sys.argv[2], sys.argv[3])
        return
    elif method == "status_transfer" and sys.argv.__len__() == 3:
        status_transfer(sys.argv[2])
        return
    elif method == "completed_transfer":
        completed_transfers()
        return
    elif method == "hide_transfer" and sys.argv.__len__() == 3:
        hide_transfer(sys.argv[2])
        return
    elif method == "status_ingest" and sys.argv.__len__() == 3:
        status_ingest(sys.argv[2])
        return
    elif method == "hide_ingest" and sys.argv.__len__() == 3:
        hide_ingest(sys.argv[2])
        return
    elif method == "waiting_ingests":
        waiting_for_user_ingests()
        return
    elif method == "completed_ingest":
        completed_ingests()
        return
    elif method == "full_reingest" and sys.argv.__len__() == 4:
        start_full_reingest(sys.argv[2], sys.argv[3])
        return
    elif method == "part_reingest" and sys.argv.__len__() == 4:
        start_partial_reingest(sys.argv[2], sys.argv[3])
        return
    else:
        raise SyntaxError('Use one of the documented keywords! You can list them with der parameter "help".')


######################################
########### MAIN PROGRAMM ############
######################################


if __name__ == "__main__":
    if sys.argv.__len__() > 1:
        init()
    else:
        raise SyntaxError('Read the f****** manual!')
    exit(0)
