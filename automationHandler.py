from os import listdir

from constants import EBOOK_SOURCE_PATH, FREIDOK_SOURCE_PATH, RETRO_SOURCE_PATH, INSERT, SOURCE
from dbHandler import db_handler


transfers = {}


def get_all_source_folder():
    list_ebook = listdir(EBOOK_SOURCE_PATH)
    insert_sources(list_ebook)
    list_retro = listdir(RETRO_SOURCE_PATH)
    insert_sources(list_retro)
    list_freidok = listdir(FREIDOK_SOURCE_PATH)
    insert_sources(list_freidok)
    return


def insert_sources(source_list):
    for item in source_list:
        db_handler(SOURCE, INSERT, item)
    return


def start_transfer():
    pass


def restart_transfer():
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
    init()
    while True:
        refresh_transfer_list()
        start_transfer()
        # Do Stuff
        pass
