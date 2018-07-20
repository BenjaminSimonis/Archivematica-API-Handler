from constants import DB_FILE, CREATE_TRANSFER_TABLE, CREATE_SOURCE_TABLE, \
    DELETE_ENTRY, INSERT_ENTRY, ALL_ENTRIES, ONE_ENTRY_UUID, ALL_SOURCES, \
    ONE_SOURCE_NAME, DELETE_SOURCE, INSERT_SOURCE
import os.path
import sqlite3


def init():
    db_exists()
    return


# Methods for the database

def create_db_connection():
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


# Methods for the transfer table
# TODO: Check, if the entry exists

def get_transfer_list():
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute(ALL_ENTRIES)
    t_list = cursor.fetchall()
    conn.close()
    return t_list


def get_transfer(uuid):
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute(ONE_ENTRY_UUID, uuid)
    transfer = cursor.fetchone()
    conn.close()
    return transfer


def delete_transfer(transfer_id):
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute(DELETE_ENTRY, transfer_id)
    conn.close()
    return


# params must be list with 7 values
# TODO: make it more complex with values from source table, update source table "transfer_started" etc
def insert_transfer(params):
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute(INSERT_ENTRY, params)
    conn.close()
    return


# Methods for the source table

def get_source_list():
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute(ALL_SOURCES)
    s_list = cursor.fetchall()
    conn.close()
    return s_list


# TODO: Check for better ways to get one source entry
def get_source(oname):
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute(ONE_SOURCE_NAME, oname)
    source = cursor.fetchone()
    conn.close()
    return source


def delete_source(source_id):
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute(DELETE_SOURCE, source_id)
    conn.close()
    return


def insert_source(oname):
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute(INSERT_SOURCE, oname)
    conn.close()
    return
