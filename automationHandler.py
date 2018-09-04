from os import listdir

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


def start_transfer_auto(name, type, accession, path):
    start_transfer(name, type, accession, path, str(AppConstants.PROCESS_AUTOMATED))
    pass


def restart_transfer_api_db():
    start_transfer()
    db_handler(AppConstants.TRANSFER, AppConstants.UPDATE_STATUS_TRANSFER)
    pass


def check_transfer_api(uuid):
    status = status_transfer(uuid) and status_ingest(uuid)
    if status == AppConstants.FAILED:
        restart_transfer_api_db()
    pass


def refresh_transfer_list_db():
    db_list = get_transfer_db()
    api_list = get_transfer_api()
    print(db_list)
    print(api_list)
    return


def check_delete_dates():
    pass


def clean_db():
    write_logs()
    pass


def write_logs(message, log_type):
    pass


def get_source_from_db():
    source_list_db = db_handler(AppConstants.SOURCE, AppConstants.GET_ALL)
    return source_list_db


def compare_source_db(list_source, list_db):
    list_new_source = {}
    for key, value in list_source.items():
        if value not in list_db:
            list_new_source[key] = value
    refresh_source_db(list_new_source)
    pass


def refresh_source_db(list_new_source):
    for key, value in list_new_source:
        success = db_handler(AppConstants.SOURCE, AppConstants.INSERT, value, key)
        if success:
            write_logs("Insert in DB from " + key + "/" + value + "was successful", "[INFO]")
        else:
            write_logs(key + "/" + value + " already exist in DB", "[ERROR]")
    return


def get_transfer_db():
    return db_handler(AppConstants.TRANSFER, AppConstants.GET_ALL)


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


if __name__ == "__main__":
    init()
    while True:
        refresh_transfer_list_db()
        start_transfer_auto()
        # Do Stuff
        pass
