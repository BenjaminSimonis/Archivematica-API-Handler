from os import listdir

from apiHandler import status_transfer, status_ingest, start_transfer
from constants import AppConstants
from dbHandler import db_handler

AppConstants = AppConstants()
transfers = {}


def get_all_source_folder():
    list_ebook = listdir(str(AppConstants.EBOOK_SOURCE_PATH))
    insert_sources(list_ebook)
    list_retro = listdir(str(AppConstants.RETRO_SOURCE_PATH))
    insert_sources(list_retro)
    list_freidok = listdir(str(AppConstants.FREIDOK_SOURCE_PATH))
    insert_sources(list_freidok)
    return


def get_all_transfers_ingests():
    t_list = db_handler(AppConstants.TRANSFER, AppConstants.GET_ALL)
    print(t_list)
    return


def insert_sources(source_list):
    for item in source_list:
        db_handler(AppConstants.SOURCE, AppConstants.INSERT, item)
    return


def start_transfer_auto(name, type, accession, path, procFile):
    status_transfer(name, type, accession, path, procFile)
    pass


def restart_transfer():
    pass


def check_transfer(uuid):
    status = status_transfer(uuid) and status_ingest(uuid)
    if status == AppConstants.FAILED:
        restart_transfer()
    pass


def refresh_transfer_list():
    pass


def check_delete_dates():
    pass


def clean_db():
    write_logs()
    pass


def write_logs():
    pass


def init():
    get_all_source_folder()
    return


if __name__ == "__main__":
    get_all_transfers_ingests()
    #init()
    #while True:
    #    refresh_transfer_list()
    #    start_transfer_auto()
    #    # Do Stuff
    #    pass
