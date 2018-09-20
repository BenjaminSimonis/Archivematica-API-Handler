from constants import AppConstants

import os.path
import sqlite3

from datetime import datetime

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
        raise Exception('\"' + db_type + '\" is not a supported type!')
    if (method is AppConstants.GET_ALL) or (method is AppConstants.GET_ONE):
        conn.close()
        return answer
    elif answer:
        conn.commit()
    else:
        conn.rollback()
    conn.close()
    return answer


def transfer_handler(cursor, method, p_list):
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
        raise Exception('\"' + method + '\" is not a supported method!')
    return answer


def source_handler(cursor, method, p_list):
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
        raise Exception('\"' + method + '\" is not a supported method!')
    return answer


##################################
# Methods for the database itself
##################################
def create_db_connection():
    db_exists()
    conn = sqlite3.connect(str(AppConstants.DB_FILE))
    return conn


def db_exists():
    if not os.path.isfile(AppConstants.DB_FILE):
        create_db()
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
        t_list = list(tuple_list[0])
        return t_list
    else:
        return tuple_list


def get_transfer(cursor, uuid):
    cursor.execute(str(AppConstants.ONE_TRANSFER_UUID), (uuid,))
    transfer = cursor.fetchone()
    return transfer


def get_active_transfers(cursor):
    cursor.execute(str(AppConstants.ACTIVE_TRANSFERS))
    active_list = cursor.fetchall()
    return active_list


def delete_transfer(cursor, transfer_id):
    cursor.execute(str(AppConstants.DELETE_TRANSFER), (transfer_id,))
    if cursor.rowcount == 1:
        return True
    else:
        raise Exception("delete_transfer:\nSomething went wrong: Rowcount = " + cursor.rowcount)


# Returns True, if no transfer already exists. Otherwise it returns the transfer ID
def exist_transfer(cursor, source_id):
    cursor.execute(str(AppConstants.ONE_TRANSFER_SOURCE_ID), (source_id,))
    transfer = cursor.fetchone()
    if transfer is not None:
        return transfer[0]
    else:
        return False


# Params: sourceID, transfername, accessionnumber, uuid, status, processingconf
def insert_transfer(cursor, params):
    if exist_transfer(cursor, params[0]) is False:
        cursor.execute(str(AppConstants.INSERT_TRANSFER), (params[0], params[1], AppConstants.TRANSFER, params[2],
                                                           params[3], params[4], params[5],))
        print(str(cursor.rowcount))
        if cursor.rowcount == 1:
            if update_source_started(cursor, params[0], 1):
                return True
    return False


# Updates the transfer status in transfer table and make rollback in sources if failed
def update_transfer_status(cursor, params):
    cursor.execute(str(AppConstants.UPDATE_STATUS_TRANSFER), (params[0], params[1],))
    if params[0] == str(AppConstants.FAILED):
        update_source_started(cursor, get_transfer(params[0], params[1])[1], -1)
    if cursor.rowcount == 1:
        return True


def update_sip_uuid_transfer(cursor, p_list):
    cursor.execute(str(AppConstants.SELECT_SIP_UUID_TRANSFER), (p_list[0],))
    transfer = list(cursor.fetchone())
    if transfer[5] is None:
        cursor.execute(AppConstants.UPDATE_SIP_UUID_TRANSFER, (p_list[1], AppConstants.INGEST, p_list[0],))
        if cursor.rowcount is 1:
            return True
        else:
            return False
    else:
        return False


################################
# Methods for the source table
################################
def get_source_list(cursor):
    cursor.execute(str(AppConstants.ALL_SOURCES))
    tuple_list = cursor.fetchall()
    if len(tuple_list) > 0:
        s_list = list(tuple_list[0])
        return s_list
    else:
        return tuple_list


def get_source(cursor, oname):
    cursor.execute(str(AppConstants.ONE_SOURCE_NAME), (oname[0],))
    source = cursor.fetchone()
    return source


def get_unstarted_source(cursor):
    cursor.execute(str(AppConstants.UNSTARTED_SOURCE))
    source = cursor.fetchone()
    return source


# Items, that will be deleted, have to be checked before calling this method
def delete_source(cursor, source_id):
    cursor.execute(str(AppConstants.DELETE_SOURCE), (source_id[0],))
    if cursor.rowcount == 1:
        return True
    else:
        raise Exception("delete_source:\nSomething went wrong: Rowcount = " + cursor.rowcount)


def update_status_source(cursor, p_list):
    cursor.execute(str(AppConstants.UPDATE_STATUS_SOURCE), (1, datetime.now(), p_list[0],))
    if cursor.rowcount == 1:
        return True
    else:
        raise Exception("delete_source:\nSomething went wrong: Rowcount = " + cursor.rowcount)


# Returns true, when insert was successful. returns false, when insert already exists
def insert_source(cursor, oname):
    if get_source(cursor, oname) is None:
        cursor.execute(str(AppConstants.INSERT_SOURCE), (oname[0], oname[1], datetime.now(),))
        if cursor.rowcount == 1:
            return True
        else:
            raise Exception('\"' + oname + '\" couldn\'t be inserted! Rowcount: ' + cursor.rowcount)
    else:
        return False


# First check the started status, then make a update. Otherwise return false
def update_source_started(cursor, source_id, started):
    cursor.execute(str(AppConstants.UPDATE_STATUS_SOURCE), (1, started, source_id,))
    if cursor.rowcount == 1:
        return True
    else:
        return False
