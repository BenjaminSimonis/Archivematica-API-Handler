from os import remove
from os.path import exists

import help
import sys

from apiHandler import start_partial_reingest, start_full_reingest, completed_ingests, \
    waiting_for_user_ingests, hide_ingest, status_ingest, hide_transfer, start_transfer, \
    list_unapproved_transfers, approve_transfer, status_transfer, completed_transfers
from constants import AppConstants
from logger import write_log


AppConstants = AppConstants()
######################################
########### Initializing #############
######################################


def init():
    method = sys.argv[1]
    if method == "help":
        if sys.argv.__len__() == 2:
            help.list_commands()
            return
        else:
            help.command_description(sys.argv[2])
            return
    elif method == "start_transfer" and sys.argv.__len__() == 7:
        write_log("manualHandler.py:\tstart_transfer: " + str(sys.argv), "[DEBUG]")
        start_transfer(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
        return
    elif method == "list_unapproved":
        write_log("manualHandler.py:\tlist_unapproved", "[DEBUG]")
        list_unapproved_transfers()
        return
    elif method == "approve_transfer" and sys.argv.__len__() == 4:
        write_log("manualHandler.py:\tapprove_transfer: " + str(sys.argv), "[DEBUG]")
        approve_transfer(sys.argv[2], sys.argv[3])
        return
    elif method == "status_transfer" and sys.argv.__len__() == 3:
        write_log("manualHandler.py:\tstatus_transfer: " + str(sys.argv), "[DEBUG]")
        status_transfer(sys.argv[2])
        return
    elif method == "completed_transfer":
        write_log("manualHandler.py:\tcompleted_transfer", "[DEBUG]")
        completed_transfers()
        return
    elif method == "hide_transfer" and sys.argv.__len__() == 3:
        write_log("manualHandler.py:\thide_transfer: " + str(sys.argv), "[DEBUG]")
        hide_transfer(sys.argv[2])
        return
    elif method == "status_ingest" and sys.argv.__len__() == 3:
        write_log("manualHandler.py:\tstatus_ingest: " + str(sys.argv), "[DEBUG]")
        status_ingest(sys.argv[2])
        return
    elif method == "hide_ingest" and sys.argv.__len__() == 3:
        write_log("manualHandler.py:\thide_ingest: " + str(sys.argv), "[DEBUG]")
        hide_ingest(sys.argv[2])
        return
    elif method == "waiting_ingests":
        write_log("manualHandler.py:\twaiting_ingests", "[DEBUG]")
        waiting_for_user_ingests()
        return
    elif method == "completed_ingest":
        write_log("manualHandler.py:\tcompleted_ingest", "[DEBUG]")
        completed_ingests()
        return
    elif method == "full_reingest" and sys.argv.__len__() == 4:
        write_log("manualHandler.py:\tfull_reingest: " + str(sys.argv), "[DEBUG]")
        start_full_reingest(sys.argv[2], sys.argv[3])
        return
    elif method == "part_reingest" and sys.argv.__len__() == 4:
        write_log("manualHandler.py:\tpart_reingest: " + str(sys.argv), "[DEBUG]")
        start_partial_reingest(sys.argv[2], sys.argv[3])
        return
    elif method == "test":
        write_log("manualHandler.py:\ttest", "[DEBUG]")
        return
    else:
        write_log("manualHandler.py\tUse one of the documented keywords! You can list them with der parameter help.", "[ERROR]")
        raise SyntaxError('Use one of the documented keywords! You can list them with der parameter "help".')


######################################
########### MAIN PROGRAM ############
######################################


if __name__ == "__main__":
    if sys.argv.__len__() > 1:
        if sys.argv[-1] == "DEBUG":
            f = open("DEBUG", "w+")
            f.close()
        else:
            if exists(str(AppConstants.DEBUG_PATH)):
                remove(str(AppConstants.DEBUG_PATH))
        init()
    else:
        write_log("manualHandler.py:\tRead the f****** manual!", "[ERROR]")
        raise SyntaxError('Read the f****** manual!')
    exit(0)
