from dbHandler import get_transfer_list, db_exists


transfers = {}


def get_all_source_folder():
    pass


def start_transfer():
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
    db_exists()
    pass


if __name__ == "__main__":
    init()
    while True:
        refresh_transfer_list()
        start_transfer()
        # Do Stuff
        pass
