# API constants
URL_API = "/api"
URL_TRANSFER = URL_API + "/transfer"
URL_INGEST = URL_API + "/ingest"

# General path constants
WORKING_PATH = "/var/archivematica"
HANDLER_PATH = WORKING_PATH + "/Archivematica-API-Handler/"
SOURCE_PATH = WORKING_PATH + "/source"
EBOOK_SOURCE_PATH = SOURCE_PATH + "/ebooks"
RETRO_SOURCE_PATH = SOURCE_PATH + "/retro"
FREIDOK_SOURCE_PATH = SOURCE_PATH + "/freidok"
DONE_SOURCE_PATH = SOURCE_PATH + "/done"

# Processing path constants
PROCESS_PATH = WORKING_PATH + "/sharedDirectory/sharedMicroServiceTasksConfigs/processingMCPConfigs/"
PROCESS_DEFAULT = "defaultProcessingMCP.xml"
PROCESS_AUTOMATED = "automatedProcessingMCP.xml"
PROCESS_PATH_AUTOMATED = PROCESS_PATH + PROCESS_AUTOMATED
PROCESS_PATH_DEFAULT = PROCESS_PATH + PROCESS_DEFAULT
LOCAL_PROCESS_DIR = "processingConfs/"

# Database constants
DB_FILE = HANDLER_PATH + "storage.db"

CREATE_TRANSFER_TABLE = "CREATE TABLE transfer (_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
                         source INTEGER NOT NULL, tname TEXT NOT NULL, \
                         acnumber INTEGER, uuid TEXT NOT NULL, status TEXT NOT NULL, \
                         failcount INTEGER DEFAULT 0, deletedate INTEGER, procconf TEXT NOT NULL, \
                         FOREIGN KEY (source) REFERENCES sources(_id));"

# TODO: Add column for transfer directory/type
# TODO: Add column timestamp, when source is added to db
CREATE_SOURCE_TABLE = "CREATE TABLE sources (_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                       oname TEXT NOT NULL, transfer_started INTEGER DEFAULT 0);"

DELETE_TRANSFER = "DELETE FROM transfer WHERE _id = ?;"
INSERT_TRANSFER = "INSERT INTO transfer (source,tname,acnumber,uuid,status,deletedate,procconf)\
                VALUES (?,?,?,?,?,?,?);"
UPDATE_STATUS_TRANSFER = "UPDATE transfer SET status = ? WHERE uuid = ?;"
ALL_TRANSFERS = "SELECT * FROM transfer;"
ONE_TRANSFER_UUID = "SELECT * FROM transfer WHERE uuid = ?;"

DELETE_SOURCE = "DELETE FROM sources WHERE _id = ?;"
INSERT_SOURCE = "INSERT INTO sources (oname) VALUES (?);"
ALL_SOURCES = "SELECT * FROM sources;"
ONE_SOURCE_NAME = "SELECT * FROM sources WHERE oname = ?;"

# Miscellaneous constants
SOURCE = "SOURCE"
TRANSFER = "TRANSFER"
GET_ALL = "GET_ALL"
GET_ONE = "GET_ONE"
INSERT = "INSERT"
DELETE = "DELETE"
