import os
from constants import AppConstants
from datetime import datetime

AppConstants = AppConstants()


def open_log_writer():
    f = open("logs/transfer.log", "a")
    return f


def open_error_writer():
    f = open("logs/error.log", "a")
    return f


def open_delete_writer():
    f = open("logs/delete.log", "a")
    return f


def create_timestamp():
    return str(datetime.now())


def debug_mode():
    if os.path.isfile(AppConstants.DEBUG_PATH):
        return True
    else:
        return False


def write_log(message, log_type):
    if log_type is "[ERROR]":
        logger = open_error_writer()
    elif log_type is "[DELETE]":
        logger = open_delete_writer()
    else:
        logger = open_log_writer()
    if (log_type == "[DEBUG]" and debug_mode()) or log_type == "[INFO]" \
            or log_type == "[ERROR]" or log_type == "[DELETE]":
        logger.write(log_type + "\t" + create_timestamp() + "\t" + message + "\n")
    logger.flush()
    logger.close()
    return True
