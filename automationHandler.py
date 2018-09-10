from os import listdir
from time import sleep

from apiHandler import status_transfer, status_ingest, start_transfer
from constants import AppConstants
from dbHandler import db_handler

AppConstants = AppConstants()
transfers = {}


# source_list = {"EBOOK" : [], "RETRO" : [], "FREIDOK" : []}
def get_all_source_folder():
    source_list = {str(AppConstants.EBOOK): listdir(str(AppConstants.EBOOK_SOURCE_PATH)),
                   str(AppConstants.RETRO): listdir(str(AppConstants.RETRO_SOURCE_PATH)),
                   str(AppConstants.FREIDOK): listdir(str(AppConstants.FREIDOK_SOURCE_PATH))}
    return source_list


def get_all_transfers_ingests_db():
    t_list = db_handler(AppConstants.TRANSFER, AppConstants.GET_ALL)
    return t_list


def insert_sources_db(source_list):
    for item in source_list:
        db_handler(AppConstants.SOURCE, AppConstants.INSERT, item)
    return


def restart_transfer_api_db():
    start_transfer()
    db_handler(AppConstants.TRANSFER, AppConstants.UPDATE_STATUS_TRANSFER)
    pass


def check_transfer_api(uuid):
    status = status_transfer(uuid) and status_ingest(uuid)
    if status == AppConstants.FAILED:
        restart_transfer_api_db()
    pass


# TODO: When db_list has entries, check for updates from API. Ignore all finished Ingests in db_list.
# TODO: Implement delete routine for new finished items from DB after check with API
# TODO: Return list of startable source items
def refresh_transfer_list_db():
    db_list = get_transfer_db()
    print(db_list)
    if len(db_list) > 0:
        # TODO: Check output of db list and look for entries in transfer db

        api_list = get_transfer_api(db_list[0])
        print(api_list)
    else:
        print("No Transfer in DB.")
    return


def check_delete_dates():
    pass


def clean_db():
    write_logs("Cleaned DB", "[INFO]")
    pass


def write_logs(message, log_type):
    print(log_type + " " + message)
    pass


def get_source_from_db():
    return db_handler(AppConstants.SOURCE, AppConstants.GET_ALL)


def get_unstarted_source_from_db():
    return db_handler(AppConstants.SOURCE, AppConstants.GET_UNSTARTED)


def compare_source_db(list_source, list_db):
    list_new_source = {}
    for key, value in list_source.items():
        if value not in list_db:
            list_new_source[key] = value
    refresh_source_db(list_new_source)
    pass


def refresh_source_db(list_new_source):
    for key in list_new_source:
        for value in list_new_source[key]:
            success = db_handler(AppConstants.SOURCE, AppConstants.INSERT, value, key)
            if success:
                write_logs("Insert in DB from " + key + "/" + value + " was successful", "[INFO]")
            else:
                write_logs(key + "/" + value + " already exist in DB", "[ERROR]")
    return


def get_transfer_db():
    return db_handler(AppConstants.TRANSFER, AppConstants.GET_ALL)


def get_active_transfers_db():
    return db_handler(AppConstants.TRANSFER, AppConstants.GET_ACTIVE)


def get_transfer_api(uuids):
    status = {}
    for uuid in uuids:
        status[str(AppConstants.TRANSFER) + "-" + uuid] = status_transfer(uuid)
        status[str(AppConstants.INGEST) + "-" + uuid] = status_ingest(uuid)
    return status


def init():
    list_db = get_source_from_db()
    list_source = get_all_source_folder()
    compare_source_db(list_source, list_db)
    refresh_transfer_list_db()
    return


def start_transfer_auto():
    if len(get_active_transfers_db()) < 2:
        new_ingest = get_unstarted_source_from_db()
        # TODO: Check Params and make new fields in source table if necessary for starting a new transfer
        start_transfer(new_ingest[1],new_ingest[2])
        #refresh_transfer_list_db()
    else:
        sleep(5)
        #refresh_transfer_list_db()

    pass


if __name__ == "__main__":
    init()
    while True:
        start_transfer_auto()
    pass
