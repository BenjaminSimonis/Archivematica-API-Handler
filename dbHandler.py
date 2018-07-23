from constants import DB_FILE, CREATE_TRANSFER_TABLE, CREATE_SOURCE_TABLE, \
    DELETE_TRANSFER, INSERT_TRANSFER, ALL_TRANSFERS, ONE_TRANSFER_UUID, ALL_SOURCES, \
    ONE_SOURCE_NAME, DELETE_SOURCE, INSERT_SOURCE, UPDATE_STATUS_TRANSFER, SOURCE, TRANSFER, GET_ALL, GET_ONE, INSERT, \
    DELETE
import os.path
import sqlite3


################################################################
# Handler for interactions with other classes
################################################################
def db_handler(db_type, method, *params):
    conn = create_db_connection()
    cursor = conn.cursor()
    if db_type == SOURCE:
        answer = source_handler(cursor, method, params)
    elif db_type == TRANSFER:
        answer = transfer_handler(cursor, method, params)
    else:
        raise Exception('\"' + db_type + '\" is not a supported type!')
    conn.commit()
    conn.close()
    return answer


def transfer_handler(cursor, method, p_list):
    answer = None
    if method == GET_ALL:
        answer = get_transfer_list(cursor)
    elif method == GET_ONE:
        answer = get_transfer(cursor, p_list)
    elif method == INSERT:
        answer = insert_transfer(cursor, p_list)
    elif method == DELETE:
        answer = delete_transfer(cursor, p_list)
    else:
        raise Exception('\"' + method + '\" is not a supported method!')
    return answer


def source_handler(cursor, method, p_list):
    answer = None
    if method == GET_ALL:
        answer = get_source_list(cursor)
    elif method == GET_ONE:
        answer = get_source(cursor, p_list)
    elif method == INSERT:
        answer = insert_source(cursor, p_list)
    elif method == DELETE:
        answer = delete_source(cursor, p_list)
    else:
        raise Exception('\"' + method + '\" is not a supported method!')
    return answer


##################################
# Methods for the database itself
##################################
def create_db_connection():
    db_exists()
    conn = sqlite3.connect(DB_FILE)
    return conn


def db_exists():
    if not os.path.isfile(DB_FILE):
        create_db()
    return


def create_db():
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute(CREATE_SOURCE_TABLE)
    cursor.execute(CREATE_TRANSFER_TABLE)
    conn.close()
    return


##################################
# Methods for the transfer table
# TODO: Check, if the entry exists
##################################
def get_transfer_list(cursor):
    cursor.execute(ALL_TRANSFERS)
    t_list = cursor.fetchall()
    return t_list


def get_transfer(cursor, uuid):
    cursor.execute(ONE_TRANSFER_UUID, uuid)
    transfer = cursor.fetchone()
    return transfer


def delete_transfer(cursor, transfer_id):
    cursor.execute(DELETE_TRANSFER, transfer_id)
    pass


# params must be list with 7 values
# TODO: make it more complex with values from source table, update source table "transfer_started" etc
def insert_transfer(cursor, params):
    cursor.execute(INSERT_TRANSFER, params)
    pass


def update_transfer_status(cursor, status, uuid):
    cursor.execute(UPDATE_STATUS_TRANSFER, (status, uuid))
    pass


################################
# Methods for the source table
################################
def get_source_list(cursor):
    cursor.execute(ALL_SOURCES)
    s_list = cursor.fetchall()
    return s_list


def get_source(cursor, oname):
    cursor.execute(ONE_SOURCE_NAME, oname[0])
    source = cursor.fetchone()
    return source


# Items, that will be deleted, have to be checked before calling this method
def delete_source(cursor, source_id):
    cursor.execute(DELETE_SOURCE, source_id[0])
    if cursor.rowcount == 1:
        return "Deletion was successful"
    else:
        raise Exception("")


def insert_source(cursor, oname):
    cursor.execute(INSERT_SOURCE, oname[0])
    if cursor.rowcount == 1:
        answer = get_source(cursor, oname)
    else:
        raise Exception('\"' + oname + '\" couldn\'t be inserted!')
    return answer


def update_source(cursor, source_id):
    pass
