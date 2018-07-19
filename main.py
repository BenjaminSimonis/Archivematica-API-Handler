import help
import processingHandler
import sys

from apiHandler import start_partial_reingest, start_full_reingest, completed_ingests, \
    waiting_for_user_ingests, hide_ingest, status_ingest, hide_transfer, start_transfer, \
    list_unapproved_transfers, approve_transfer, status_transfer, completed_transfers


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
        start_transfer(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
        return
    elif method == "list_unapproved":
        list_unapproved_transfers()
        return
    elif method == "approve_transfer" and sys.argv.__len__() == 4:
        approve_transfer(sys.argv[2], sys.argv[3])
        return
    elif method == "status_transfer" and sys.argv.__len__() == 3:
        status_transfer(sys.argv[2])
        return
    elif method == "completed_transfer":
        completed_transfers()
        return
    elif method == "hide_transfer" and sys.argv.__len__() == 3:
        hide_transfer(sys.argv[2])
        return
    elif method == "status_ingest" and sys.argv.__len__() == 3:
        status_ingest(sys.argv[2])
        return
    elif method == "hide_ingest" and sys.argv.__len__() == 3:
        hide_ingest(sys.argv[2])
        return
    elif method == "waiting_ingests":
        waiting_for_user_ingests()
        return
    elif method == "completed_ingest":
        completed_ingests()
        return
    elif method == "full_reingest" and sys.argv.__len__() == 4:
        start_full_reingest(sys.argv[2], sys.argv[3])
        return
    elif method == "part_reingest" and sys.argv.__len__() == 4:
        start_partial_reingest(sys.argv[2], sys.argv[3])
        return
    elif method == "test":
        processingHandler.compare_processing_file(sys.argv[2])
        return
    else:
        raise SyntaxError('Use one of the documented keywords! You can list them with der parameter "help".')


######################################
########### MAIN PROGRAMM ############
######################################


if __name__ == "__main__":
    if sys.argv.__len__() > 1:
        init()
    else:
        raise SyntaxError('Read the f****** manual!')
    exit(0)
