import subprocess

from constants import AppConstants
from logger import write_log

AppConstants = AppConstants()


def add_conf_file(ingest_folder, conf):
    if conf is AppConstants.AUTOMATED:
        print()
    else:
        print()
    write_log("processingHandler.py:\t" + "Added " + str(conf) + " conf file to " + str(ingest_folder), "[DEBUG]")
    pass
