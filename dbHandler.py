import os.path
import sqlite3

from datetime import datetime

from constants import AppConstants
from logger import write_log

AppConstants = AppConstants()


# TODO: Replace Exceptions with ErrorLogEntries and try again routine
# TODO: Write Successful Updates, Inserts, etc. in a DebugLog
# TODO: All Ingests and Transfers are Transfers in DB
# TODO: update Functions

################################################################
# Handler for interactions with other classes
################################################################

# GET-Methods returns a result, any other method returns a True or raise an Exception
def db_handler(db_type, method, *params):
    conn = create_db_connection()
    cursor = conn.cursor()
    if db_type == AppConstants.SOURCE:
        answer = source_handler(cursor, method, params)
    elif db_type == AppConstants.TRANSFER:
        answer = transfer_handler(cursor, method, params)
    else:
        write_log('dbHandler.py:\t\"' + db_type + '\" is not a supported type!', "[ERROR]")
    if (method is AppConstants.GET_ALL) or (method is AppConstants.GET_ONE):
        conn.close()
        write_log("dbHandler.py:\tSelected from " + db_type + ": " + answer, "[DEBUG]")
        return answer
    elif answer:
        write_log("dbHandler.py:\tCommitted changes.", "[DEBUG]")
        conn.commit()
    else:
        write_log("dbHandler.py:\tUndo changes.", "[DEBUG]")
        conn.rollback()
    conn.close()
    return answer


def transfer_handler(cursor, method, p_list):
    write_log("dbHandler.py:\ttransfer_handler: " + method, "[DEBUG]")
    if method == AppConstants.GET_ALL:
        answer = get_transfer_list(cursor)
    elif method == AppConstants.GET_ONE:
        answer = get_transfer(cursor, p_list)
    elif method == AppConstants.GET_ACTIVE:
        answer = get_active_transfers(cursor)
    elif method == AppConstants.INSERT:
        answer = insert_transfer(cursor, p_list)
    elif method == AppConstants.DELETE:
        answer = delete_transfer(cursor, p_list)
    elif method == AppConstants.UPDATE_SIP_UUID_TRANSFER:
        answer = update_sip_uuid_transfer(cursor, p_list)
    elif method == AppConstants.UPDATE_STATUS_TRANSFER:
        answer = update_transfer_status(cursor, p_list)
    else:
        write_log('dbHandler.py\t\"' + method + '\" is not a supported method!', "[ERROR]")
    return answer


def source_handler(cursor, method, p_list):
    write_log("dbHandler.py:\tsource_handler: " + method, "[DEBUG]")
    if method == AppConstants.GET_ALL:
        answer = get_source_list(cursor)
    elif method == AppConstants.GET_ONE:
        answer = get_source(cursor, p_list)
    elif method == AppConstants.GET_UNSTARTED:
        answer = get_unstarted_source(cursor)
    elif method == AppConstants.INSERT:
        answer = insert_source(cursor, p_list)
    elif method == AppConstants.UPDATE_STATUS_SOURCE:
        answer = update_status_source(cursor, p_list)
    elif method == AppConstants.DELETE:
        answer = delete_source(cursor, p_list)
    else:
        write_log('dbHandler.py:\t\"' + method + '\" is not a supported method!', "[ERROR]")
    return answer


##################################
# Methods for the database itself
##################################
def create_db_connection():
    db_exists()
    conn = sqlite3.connect(str(AppConstants.DB_FILE))
    write_log("dbHandler.py:\tCreate DB Connection.", "[DEBUG]")
    return conn


def db_exists():
    if not os.path.isfile(AppConstants.DB_FILE):
        write_log("dbHandler.py:\tNo DB found.", "[INFO]")
        create_db()
        write_log("dbHandler.py:\tNew DB created.", "[INFO]")
    return


def create_db():
    conn = sqlite3.connect(str(AppConstants.DB_FILE))
    cursor = conn.cursor()
    cursor.execute(str(AppConstants.CREATE_SOURCE_TABLE))
    cursor.execute(str(AppConstants.CREATE_TRANSFER_TABLE))
    conn.commit()
    conn.close()
    return


##################################
# Methods for the transfer table
##################################
def get_transfer_list(cursor):
    cursor.execute(str(AppConstants.ALL_TRANSFERS))
    tuple_list = cursor.fetchall()
    if len(tuple_list) > 0:
        t_list = list(tuple_list)
        write_log("dbHandler.py:\tget_transfer_list: " + tuple_list, "[DEBUG]")
        return t_list
    else:
        write_log("dbHandler.py:\tget_transfer_list: " + tuple_list, "[DEBUG]")
        return tuple_list


def get_transfer(cursor, uuid):
    cursor.execute(str(AppConstants.ONE_TRANSFER_UUID), (uuid,))
    transfer = cursor.fetchone()
    write_log("dbHandler.py:\tget_transfer: " + transfer, "[DEBUG]")
    return transfer


def get_active_transfers(cursor):
    cursor.execute(str(AppConstants.ACTIVE_TRANSFERS))
    active_list = cursor.fetchall()
    write_log("dbHandler.py:\tget_active_transfers: " + active_list, "[DEBUG]")
    return active_list


def delete_transfer(cursor, transfer_id):
    cursor.execute(str(AppConstants.DELETE_TRANSFER), (transfer_id,))
    if cursor.rowcount == 1:
        write_log("dbHandler.py:\tdelete_transfer:\tDeletion was successful for transfer_id " + transfer_id, "[INFO]")
        return True
    else:
        write_log("dbHandler.py:\tdelete_transfer:\tSomething went wrong: Rowcount = " + cursor.rowcount, "[ERROR]")


# Returns True, if no transfer already exists. Otherwise it returns the transfer ID
def exist_transfer(cursor, source_id):
    cursor.execute(str(AppConstants.ONE_TRANSFER_SOURCE_ID), (source_id,))
    transfer = cursor.fetchone()
    if transfer is not None:
        write_log("dbHandler.py:\texist_transfer:\tTransfer already exist: " + transfer, "[DEBUG]")
        return transfer[0]
    else:
        write_log("dbHandler.py:\texist_transfer:\tTransfer doesn't exist.", "[DEBUG]")
        return False


# Params: sourceID, transfername, accessionnumber, uuid, status, processingconf
def insert_transfer(cursor, params):
    if exist_transfer(cursor, params[0]) is False:
        cursor.execute(str(AppConstants.INSERT_TRANSFER), (params[0], params[1], AppConstants.TRANSFER, params[2],
                                                           params[3], params[4], params[5],))
        if cursor.rowcount == 1:
            if update_source_started(cursor, params[0], 1):
                write_log("dbHandler.py:\tinsert_transfer:\tInserted: " + params, "[INFO]")
                return True
    write_log("dbHandler.py:\tinsert_transfer:\tInsert failed: " + params, "[INFO]")
    return False


# Updates the transfer status in transfer table and make rollback in sources if failed
def update_transfer_status(cursor, params):
    cursor.execute(str(AppConstants.UPDATE_STATUS_TRANSFER), (params[0], params[1],))
    if params[0] == str(AppConstants.FAILED):
        update_source_started(cursor, get_transfer(params[0], params[1])[1], -1)
    if cursor.rowcount == 1:
        write_log("dbHandler.py:\tupdate_transfer_status:\t" + params, "[INFO]")
        return True


def update_sip_uuid_transfer(cursor, p_list):
    cursor.execute(str(AppConstants.SELECT_SIP_UUID_TRANSFER), (p_list[0],))
    transfer = list(cursor.fetchone())
    if transfer[6] is None:
        cursor.execute(AppConstants.UPDATE_SIP_UUID_TRANSFER, (p_list[1], AppConstants.INGEST, p_list[0],))
        if cursor.rowcount is 1:
            write_log("dbHandler.py:\tupdate_sip_uuid_transfer:\tUpdate Successful: " + p_list, "[INFO]")
            return True
        else:
            write_log("dbHandler.py:\tupdate_sip_uuid_transfer:\tUpdate failed: " + p_list, "[INFO]")
            return False
    else:
        write_log("dbHandler.py:\tupdate_sip_uuid_transfer:\tTransfer has already a SIP UUID: " + p_list, "[DEBUG]")
        return True


################################
# Methods for the source table
################################
def get_source_list(cursor):
    cursor.execute(str(AppConstants.ALL_SOURCES))
    tuple_list = cursor.fetchall()
    if len(tuple_list) > 0:
        s_list = list(tuple_list)
        write_log("dbHandler.py:\tget_source_list:\t" + tuple_list, "[DEBUG]")
        return s_list
    else:
        write_log("dbHandler.py:\tget_source_list:\t" + tuple_list, "[DEBUG]")
        return tuple_list


def get_source(cursor, oname):
    cursor.execute(str(AppConstants.ONE_SOURCE_NAME), (oname[0],))
    source = cursor.fetchone()
    write_log("dbHandler.py:\tget_source:\t" + source, "[DEBUG]")
    return source


def get_unstarted_source(cursor):
    cursor.execute(str(AppConstants.UNSTARTED_SOURCE))
    source = cursor.fetchone()
    write_log("dbHandler.py:\tget_unstarted_source:\t" + source, "[DEBUG]")
    return source


# Items, that will be deleted, have to be checked before calling this method
def delete_source(cursor, source_id):
    cursor.execute(str(AppConstants.DELETE_SOURCE), (source_id[0],))
    if cursor.rowcount == 1:
        write_log("dbHandler.py:\tdelete_source:\tDeletion was successful for source_id " + source_id, "[INFO]")
        return True
    else:
        write_log("dbHandler.py:\tdelete_source:\tSomething went wrong: Rowcount = " + cursor.rowcount, "[ERROR]")
        return False


def update_status_source(cursor, p_list):
    cursor.execute(str(AppConstants.UPDATE_STATUS_SOURCE), (1, datetime.now(), p_list[0],))
    if cursor.rowcount == 1:
        return True
    else:
        write_log("dbHandler.py:\tupdate_status_source:\tSomething went wrong: Rowcount = " + cursor.rowcount, "[ERROR]")
        return False


# Returns true, when insert was successful. returns false, when insert already exists
def insert_source(cursor, oname):
    if get_source(cursor, oname) is None:
        cursor.execute(str(AppConstants.INSERT_SOURCE), (oname[0], oname[1], datetime.now(),))
        if cursor.rowcount == 1:
            write_log("dbHandler.py:\tinsert_source:\tInserted: " + oname, "[INFO]")
            return True
        else:
            write_log('dbHandler.py:\t\"' + oname + '\" couldn\'t be inserted! Rowcount: ' + cursor.rowcount, "[ERROR]")
            return False
    else:
        write_log("dbHandler.py:\tinsert_source:\tSource already exist: " + oname, "[DEBUG]")
        return False


# First check the started status, then make a update. Otherwise return false
def update_source_started(cursor, source_id, started):
    cursor.execute(str(AppConstants.UPDATE_STATUS_SOURCE), (1, started, source_id,))
    if cursor.rowcount == 1:
        write_log("dbHandler.py:\tupdate_source_started:\t" + source_id + " - " + started, "[INFO]")
        return True
    else:
        write_log("dbHandler.py:\tupdate_source_started:\tFailed updating: " + source_id + " - " + started, "[INFO]")
        return False
