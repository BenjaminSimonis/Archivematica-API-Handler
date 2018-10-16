import json
import sys

from os import remove, listdir
from os.path import exists
from shutil import move
from time import sleep

from apiHandler import status_transfer, status_ingest, start_transfer
from constants import AppConstants
from dbHandler import db_handler
from logger import write_log

AppConstants = AppConstants()


def get_all_transfers_ingests_db():
    t_list = db_handler(AppConstants.TRANSFER, AppConstants.GET_ALL)
    return t_list


def insert_sources_db(source_list):
    for item in source_list:
        db_handler(AppConstants.SOURCE, AppConstants.INSERT, item)
    return


def insert_transfer_db(s_id, s_name, acnumber, uuid, status, conf):
    return db_handler(AppConstants.TRANSFER, AppConstants.INSERT, s_id, s_name, acnumber, uuid, status, conf)


def restart_transfer_api_db(t_uuid):
    failed_transfer = db_handler(AppConstants.TRANSFER, AppConstants.ONE_TRANSFER_UUID, t_uuid)
    if failed_transfer[10] <= 2:
        start_transfer_api(failed_transfer)
    else:
        failed_source = db_handler(AppConstants.SOURCE, AppConstants.ONE_SOURCE_ID, failed_transfer[1])
        path_failed_source = str(AppConstants.SOURCE_LIST[failed_source[2]]) + "/" + str(failed_source[1])
        if exists(path_failed_source):
            write_log("Ingest " + t_uuid + " failed too often. Please check source!", "[FAILED]")
            move(path_failed_source, str(AppConstants.FAILED_SOURCE_PATH))
    return


# TODO: When db_list has entries, check for updates from API. Ignore all finished Ingests in db_list.
# TODO: Implement delete routine for new finished items from DB after check with API
def refresh_transfer_list_db():
    db_list = get_transfer_db()
    if len(db_list) > 0:
        for item in db_list:
            transfer_item = get_transfer_api(item[5])
            db_handler(AppConstants.TRANSFER, AppConstants.UPDATE_STATUS_TRANSFER, transfer_item["status"], item[5])
            if transfer_item["status"] is AppConstants.FAILED:
                restart_transfer_api_db(item[5])
    else:
        write_log("No Transfer in DB.", "[INFO]")
    return


def check_delete_dates():
    pass


def clean_db():
    write_log("Cleaned DB", "[INFO]")
    pass


def get_sources_from_db():
    return db_handler(AppConstants.SOURCE, AppConstants.GET_ALL)


def get_unstarted_source_from_db():
    return db_handler(AppConstants.SOURCE, AppConstants.GET_UNSTARTED)


def compare_source_db(list_source, list_db):
    list_new_source = {}
    for key, value in list_source.items():
        if (value not in list_db) and is_source_dir_not_empty(key, value):
            list_new_source[key] = value
    refresh_source_db(list_new_source)
    return


def is_source_dir_not_empty(key, value):
    if len(listdir(str(AppConstants.SOURCE_DICT[key] + "/" + value))) > 0:
        return True
    else:
        return False


def refresh_source_db(list_new_source):
    for key in list_new_source:
        for value in list_new_source[key]:
            success = db_handler(AppConstants.SOURCE, AppConstants.INSERT, value, key)
            if success:
                write_log("Insert in DB from " + str(key) + "/" + str(value) + " was successful", "[INFO]")
            else:
                write_log(str(key) + "/" + str(value) + " already exist in DB", "[DEBUG]")
    return


def get_transfer_db():
    return db_handler(AppConstants.TRANSFER, AppConstants.GET_ALL)


def get_active_transfers_db():
    refresh_transfer_list_db()
    return db_handler(AppConstants.TRANSFER, AppConstants.GET_ACTIVE)


# Returns JSON Body of an UUID from transfer or ingest tab, when available
def get_transfer_api(uuid):
    t_status = json.loads(status_transfer(uuid).text)
    if "sip_uuid" in t_status:
        if db_handler(AppConstants.TRANSFER, AppConstants.UPDATE_SIP_UUID_TRANSFER, uuid, t_status["sip_uuid"]):
            return json.loads(status_ingest(t_status["sip_uuid"]).text)
    else:
        return t_status


def update_source(id):
    return db_handler(AppConstants.SOURCE, AppConstants.UPDATE_STATUS_SOURCE, id)


def start_transfer_auto():
    if len(get_active_transfers_db()) < 2:
        start_transfer_api(None)
    else:
        sleep(5)
    pass


def start_transfer_api(*transfer):
    if not transfer:
        new_ingest = get_unstarted_source_from_db()
    else:
        new_ingest = transfer
    if new_ingest is not None:
        r = start_transfer(new_ingest[1], new_ingest[2], new_ingest[0],
                           (str(AppConstants.SOURCE_DICT[new_ingest[2]]) + "/" + new_ingest[1]),
                           AppConstants.PROCESS_AUTOMATED)
        if r is not None:
            if r["status"] == 200:
                if update_source(new_ingest[0]):
                    write_log("Update source was successful - " + str(new_ingest), "[INFO]")
                if insert_transfer_db(new_ingest[0], new_ingest[1], new_ingest[0], r["uuid"], AppConstants.PROCESSING,
                                      AppConstants.PROCESS_AUTOMATED):
                    write_log("Update transfer in DB was successful - " + str(new_ingest), "[INFO]")
            else:
                write_log("Status Code: " + str(r["status"]) + " " + str(r.values()), "[ERROR]")
    return


def init():
    list_db = get_sources_from_db()
    list_source = AppConstants.SOURCE_LIST
    compare_source_db(list_source, list_db)
    refresh_transfer_list_db()
    return


def check_debug_mode():
    if sys.argv[-1] == "DEBUG":
        f = open("DEBUG", "w+")
        f.close()
    else:
        if exists(str(AppConstants.DEBUG_PATH)):
            remove(str(AppConstants.DEBUG_PATH))
    return


if __name__ == "__main__":
    check_debug_mode()
    init()
    while True:
        start_transfer_auto()
        init()
    pass
