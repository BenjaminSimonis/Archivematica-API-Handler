import logging
import os
from constants import AppConstants
from datetime import datetime

AppConstants = AppConstants()

def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)

def open_log_writer():
    setup_logger(AppConstants.GENERAL, AppConstants.LOG_PATH_GENERAL)
    return logging.getLogger(AppConstants.GENERAL)


def open_error_writer():
    setup_logger(AppConstants.ERROR, AppConstants.LOG_PATH_ERROR)
    return logging.getLogger(AppConstants.ERROR)


def open_delete_writer():
    setup_logger(AppConstants.DELETE, AppConstants.LOG_PATH_DELETE)
    return logging.getLogger(AppConstants.DELETE)


def open_debug_writer():
    setup_logger(AppConstants.DEBUG, AppConstants.LOG_PATH_DEBUG)
    return logging.getLogger(AppConstants.DEBUG)


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
    elif log_type is "[DEBUG]":
        logger = open_debug_writer()
    else:
        logger = open_log_writer()
    if (log_type == "[DEBUG]" and debug_mode()) or log_type == "[INFO]" \
            or log_type == "[ERROR]" or log_type == "[DELETE]":
        logger.info(log_type + ":\t" + message + "\n")
    return True
