from shutil import copy

from constants import AppConstants
from logger import write_log

AppConstants = AppConstants()


def add_conf_file(transfer_folder, conf):
    if conf is AppConstants.AUTOMATED:
        copy(AppConstants.PROCESS_PATH_AUTOMATED, transfer_folder)
    else:
        copy(AppConstants.PROCESS_PATH_DEFAULT, transfer_folder)
    write_log("processingHandler.py:\t" + "Added " + str(conf) + " conf file to " + str(transfer_folder), "[DEBUG]")
    pass
