from os import listdir

from apiHandler import status_transfer, status_ingest, start_transfer
from constants import AppConstants
from dbHandler import db_handler

AppConstants = AppConstants()
transfers = {}


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


def start_transfer_auto(name, type, accession, path, procFile):
    status_transfer(name, type, accession, path, procFile)
    pass


def restart_transfer_api_db():
    pass


def check_transfer_api(uuid):
    status = status_transfer(uuid) and status_ingest(uuid)
    if status == AppConstants.FAILED:
        restart_transfer_api_db()
    pass


def refresh_transfer_list_db():
    pass


def check_delete_dates():
    pass


def clean_db():
    write_logs()
    pass


def write_logs():
    pass


def get_source_from_db():
    source_list_db = db_handler(AppConstants.SOURCE, AppConstants.GET_ALL)
    return source_list_db


def compare_source_db(list_source, list_db):
    #TODO: compare source list with DB and refresh DB entries for sources
    refresh_source_db()
    pass


def refresh_source_db():
    pass


def get_transfer_db():
    pass


def get_transfer_api():
    pass


def init():
    list_db = get_source_from_db()
    list_source = get_all_source_folder()
    compare_source_db(list_source, list_db)
    get_transfer_db()
    get_transfer_api()
    return


if __name__ == "__main__":
    init()
    while True:
        refresh_transfer_list_db()
        start_transfer_auto()
        # Do Stuff
        pass
