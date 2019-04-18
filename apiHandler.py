#!/usr/bin/env python
import base64
import json
import requests

import os
from time import sleep

from constants import AppConstants
from credentials import *
from logger import write_log
AppConstants = AppConstants()


######################################
########### Transfer API #############
######################################


# URL: /api/transfer/start_transfer/
# Verb: POST
# Start a transfer
# Parameters: JSON body
# Response: JSON
def start_transfer(name, type, accession, path, procFile):
    url = str(AppConstants.URL_TRANSFER) + "/start_transfer/"
    write_log("apiHandler.py:\tStarting Transfer", "[INFO]")
    dataset = {"name": name, "type": type, "accession": accession, "paths[]": [create_base64_path(path)],
               "row_ids[]": [""]}
    write_log("apiHandler.py:\t" + str(dataset), "[DEBUG]")
    return start_and_approve(post_request(url, dataset))


# URL: /api/transfer/unapproved
# Verb: GET
# Returns a list of transfers waiting for approval.
# Response: JSON
def list_unapproved_transfers():
    url = str(AppConstants.URL_TRANSFER) + "/unapproved"
    write_log("apiHandler.py:\tList unapproved Transfers", "[INFO]")
    return get_request(url)


# URL: /api/transfer/approve
# Verb: POST
# Approve a transfer waiting to be started.
# Parameters: JSON body
# Response: JSON
def approve_transfer(type, dir):
    url = str(AppConstants.URL_TRANSFER) + "/approve"
    write_log("apiHandler.py:\tApprove Transfer", "[INFO]")
    dataset = {"type": type, "directory": dir}
    write_log("apiHandler.py:\t" + str(dataset), "[DEBUG]")
    return post_request(url, dataset)


# URL: /api/transfer/status/<transfer UUID>/
# Verb: GET
# Returns the status of the transfer.
# Response: JSON
def status_transfer(uuid):
    url = str(AppConstants.URL_TRANSFER) + "/status/" + uuid
    write_log("apiHandler.py:\tStatus Transfer: " + str(uuid), "[INFO]")
    return get_request(url)


# URL: /api/transfer/<transfer UUID>/delete/
# Verb: DELETE
# Hide a transfer
# Response: JSON
def hide_transfer(uuid):
    url = str(AppConstants.URL_TRANSFER) + "/" + uuid + "/delete/"
    write_log("apiHandler.py:\tHide Transfer: " + str(uuid), "[INFO]")
    return delete_request(url)


# URL: /api/transfer/completed/
# Verb: GET
# Return list of Transfers that are completed
# Response: JSON
def completed_transfers():
    url = str(AppConstants.URL_TRANSFER) + "/completed/"
    write_log("apiHandler.py:\tCompleted Transfers", "[INFO]")
    return get_request(url)


######################################
############ Ingest API ##############
######################################


# URL: /ingest/status/<unit UUID>/
# Verb: GET
# Returns the status of the SIP
# Response: JSON
def status_ingest(uuid):
    url = str(AppConstants.URL_INGEST) + "/status/" + uuid + "/"
    write_log("apiHandler.py:\tStatus Ingest: " + str(uuid), "[INFO]")
    return get_request(url)


# URL: /api/ingest/<SIP UUID>/delete/
# Verb: DELETE
# Hide a SIP
# Response: JSON
def hide_ingest(uuid):
    url = str(AppConstants.URL_INGEST) + "/" + uuid + "/delete/"
    write_log("apiHandler.py:\tHide Ingest: " + str(uuid), "[INFO]")
    return delete_request(url)


# URL: /api/ingest/waiting
# Verb: GET
# Returns a list of SIPs waiting for user input.
# Response: JSON
def waiting_for_user_ingests():
    url = str(AppConstants.URL_INGEST) + "/waiting"
    write_log("apiHandler.py:\tIngests waiting for user input", "[INFO]")
    return get_request(url)


# URL: /api/ingest/completed/
# Verb: GET
# Return list of SIPs that are completed
# Response: JSON
def completed_ingests():
    url = str(AppConstants.URL_INGEST) + "/completed/"
    write_log("apiHandler.py:\tCompleted Ingests", "[INFO]")
    return get_request(url)


# URL: /api/transfer/reingest
# Verb: POST
# Start a full reingest.
# Parameters: JSON body
# Response: JSON
def start_full_reingest(name, uuid):
    url = str(AppConstants.URL_TRANSFER) + "/reingest"
    write_log("apiHandler.py:\tFull Re-Ingest", "[INFO]")
    dataset = {"name": name, "uuid": uuid}
    write_log("apiHandler.py:\t" + str(dataset), "[DEBUG]")
    return post_request(url, dataset)


# URL: /api/ingest/reingest
# Verb: POST
# Start a partial or metadata-only reingest.
# Parameters: JSON body
# Response: JSON
def start_partial_reingest(name, uuid):
    url = str(AppConstants.URL_INGEST) + "/reingest"
    write_log("apiHandler.py:\tFull Re-Ingest", "[INFO]")
    dataset = {"name": name, "uuid": uuid}
    write_log("apiHandler.py:\t" + str(dataset), "[DEBUG]")
    return post_request(url, dataset)


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

# Encode the path for a package in base64 format
def create_base64_path(target_path):
    if target_path == "":
        path = str(AppConstants.SOURCE_PATH)
    else:
        path = target_path
    base_path = base64.b64encode(os.fsencode(TS_LOCATION_UUID) + b':' + os.fsencode(path))
    write_log("apiHandler.py:\t" + str(base_path), "[DEBUG]")
    return base_path


######################################
######### Processing Calls ###########
######################################

# Start a new transfer, wait for 5 seconds, get a list of unapproved transfers and approve the one that was started
def start_and_approve(r):
    raw_json_start = json.loads(r.text)
    start_dir_name = raw_json_start["path"].split("/")[-2]
    sleep(5)
    unapproved_transfers = json.loads(list_unapproved_transfers().text)
    for result in unapproved_transfers["results"]:
        if result["directory"] == start_dir_name:
            response = approve_transfer(result["type"], start_dir_name)
            resp_dict = {"status": response.status_code, "message": json.loads(response.text)["message"],
                         "uuid": json.loads(response.text)["uuid"]}
            write_log("apiHandler.py:\t" + str(resp_dict), "[DEBUG]")
            return resp_dict
        else:
            continue
    return


######################################
####### Postprocessing Calls #########
######################################

# If something went wrong raise an exception
def process_response(r):
    if r.status_code == 200:
        write_log("apiHandler.py:\tSuccess! - Status Code: " + str(r.status_code) + "Response: " + str(r.text), "[DEBUG]")
    else:
        write_log("apiHandler.py:\tFailed! - Status Code: " + str(r.status_code) + "Response: " + str(r.reason), "[DEBUG]")
    return
