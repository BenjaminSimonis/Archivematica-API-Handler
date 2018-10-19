from os import listdir


class AppConstants:

    #########################################
    ########## Init of Properties ###########
    #########################################

    def __init__(self):
        # API constants
        self._URL_API = "/api"
        self._URL_TRANSFER = self._URL_API + "/transfer"
        self._URL_INGEST = self._URL_API + "/ingest"

        # General path constants
        self._WORKING_PATH = "/var/archivematica"
        self._HANDLER_PATH = self._WORKING_PATH + "/Archivematica-API-Handler/"
        self._SOURCE_PATH = self._WORKING_PATH + "/source"
        self._DONE_SOURCE_PATH = self._SOURCE_PATH + "/done"
        self._FAILED_SOURCE_PATH = self._SOURCE_PATH + "/failed"

        ########################
        # Installations specific constants (please edit for own installation)
        ########################
        self._EBOOK_SOURCE_PATH = self._SOURCE_PATH + "/ebooks"
        self._RETRO_SOURCE_PATH = self._SOURCE_PATH + "/retro"
        self._REPO_SOURCE_PATH = self._SOURCE_PATH + "/repo"
        self._EBOOK = "EBOOK"
        self._RETRO = "RETRO"
        self._REPO = "REPO"
        # Dict constants
        self._SOURCE_DICT = {str(self.REPO): str(self.REPO_SOURCE_PATH),
                             str(self.RETRO): str(self.RETRO_SOURCE_PATH),
                             str(self.EBOOK): str(self.EBOOK_SOURCE_PATH)}
        ##########################

        # Processing path constants
        self._PROCESS_PATH = self._WORKING_PATH + "/sharedDirectory/sharedMicroServiceTasksConfigs/processingMCPConfigs/"
        self._PROCESS_DEFAULT = "defaultProcessingMCP.xml"
        self._PROCESS_AUTOMATED = "automatedProcessingMCP.xml"
        self._PROCESS_PATH_AUTOMATED = self._PROCESS_PATH + self._PROCESS_AUTOMATED
        self._PROCESS_PATH_DEFAULT = self._PROCESS_PATH + self._PROCESS_DEFAULT
        self._LOCAL_PROCESS_DIR = "processingConfs/"

        self._DEBUG_FILE = "DEBUG"
        self._DEBUG_PATH = self._HANDLER_PATH + self._DEBUG_FILE

        # Miscellaneous constants
        self._SOURCE = "SOURCE"
        self._TRANSFER = "TRANSFER"
        self._INGEST = "INGEST"
        self._GET_ALL = "GET_ALL"
        self._GET_ONE = "GET_ONE"
        self._GET_ACTIVE = "GET_ACTIVE"
        self._GET_UNSTARTED = "GET_UNSTARTED"
        self._INSERT = "INSERT"
        self._DELETE = "DELETE"
        self._FAILED = "FAILED"
        self._REJECTED = "REJECTED"
        self._USER_INPUT = "USER_INPUT"
        self._COMPLETE = "COMPLETE"
        self._PROCESSING = "PROCESSING"
        self._TYPE_TRANSFER = "transfer"
        self._TYPE_INGEST = "SIP"

        # Database constants
        self._DB_FILE = self._HANDLER_PATH + "storage.db"

        # TODO: type + failed entfernen, abhängigkeiten prüfen, Arrays mit neuen zahlen beschreiben
        self._CREATE_TRANSFER_TABLE = "CREATE TABLE transfer (_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
                                 source INTEGER NOT NULL, tname TEXT NOT NULL, type TEXT NOT NULL,\
                                 acnumber INTEGER, t_uuid TEXT NOT NULL, i_uuid TEXT, status TEXT NOT NULL, \
                                 deletedate INTEGER, procconf TEXT NOT NULL, \
                                 FOREIGN KEY (source) REFERENCES sources(_id));"

        # TODO: Add column ingest_finished
        self._CREATE_SOURCE_TABLE = "CREATE TABLE sources (_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                                oname TEXT NOT NULL, type TEXT NOT NULL, inserted timestamp NOT NULL, \
                                transfer_started INTEGER DEFAULT 0, started timestamp);"

        # Transfer Table Queries
        self._DELETE_TRANSFER = "DELETE FROM transfer WHERE _id = ?;"
        self._INSERT_TRANSFER = "INSERT INTO transfer (source,tname,type,acnumber,t_uuid,status,procconf)\
                        VALUES (?,?,?,?,?,?,?);"
        self._UPDATE_STATUS_TRANSFER = "UPDATE transfer SET status = ? WHERE t_uuid = ?;"
        self._ALL_TRANSFERS = "SELECT * FROM transfer;"
        self._ALL_NOT_COMPLETED_TRANSFERS = 'SELECT * FROM transer WHERE NOT status = "' + str(self.COMPLETE) + '";'
        self._ALL_PROCESSING_TRANSFERS = 'SELECT * FROM transfer WHERE status = "' + str(self.PROCESSING) + '";'
        self._ONE_TRANSFER_UUID = "SELECT * FROM transfer WHERE t_uuid = ?;"
        self._ONE_TRANSFER_SOURCE_ID = "SELECT * FROM transfer WHERE source = ?;"
        self._ACTIVE_TRANSFERS = 'SELECT * FROM transfer WHERE status = "' + str(self.PROCESSING) + '";'
        self._SELECT_SIP_UUID_TRANSFER = "SELECT * FROM transfer WHERE t_uuid = ?;"
        self._UPDATE_SIP_UUID_TRANSFER = "UPDATE transfer SET i_uuid = ?, type = ? WHERE t_uuid = ?;"
        self._COUNT_FAILED_TRANSFER = 'SELECT COUNT(*) FROM transfer WHERE status = "' + str(self.FAILED) + '" AND source = ?;'

        # Source Table Queries
        self._DELETE_SOURCE = "DELETE FROM sources WHERE _id = ?;"
        self._INSERT_SOURCE = "INSERT INTO sources (oname,type,inserted) VALUES (?,?,?);"
        self._UPDATE_STATUS_SOURCE = "UPDATE sources SET transfer_started = ?, started = ? WHERE _id = ?;"
        self._ALL_SOURCES = "SELECT * FROM sources;"
        self._ONE_SOURCE_NAME = "SELECT * FROM sources WHERE oname = ?;"
        self._ONE_SOURCE_ID = "SELECT * FROM sources WHERE _id = ?;"
        self._UNSTARTED_SOURCE = "SELECT * FROM sources WHERE transfer_started = 0;"

        # List constants
        self._STATUS_LIST = [str(self.FAILED), str(self.REJECTED), str(self.USER_INPUT), str(self.COMPLETE),
                             str(self.PROCESSING)]


#########################################
############## Properties ###############
#########################################

    ########################
    # Installations specific constants (please edit for own installation)
    ########################
    @property
    def EBOOK(self):
        return self._EBOOK

    @property
    def RETRO(self):
        return self._RETRO

    @property
    def REPO(self):
        return self._REPO

    @property
    def EBOOK_SOURCE_PATH(self):
        return self._EBOOK_SOURCE_PATH

    @property
    def RETRO_SOURCE_PATH(self):
        return self._RETRO_SOURCE_PATH

    @property
    def REPO_SOURCE_PATH(self):
        return self._REPO_SOURCE_PATH

    @property
    def SOURCE_LIST(self):
        source_list = {str(self._EBOOK): listdir(str(self._EBOOK_SOURCE_PATH)),
                       str(self._RETRO): listdir(str(self._RETRO_SOURCE_PATH)),
                       str(self._REPO): listdir(str(self._REPO_SOURCE_PATH))}
        return source_list

    ##############################################################

    # API constants

    @property
    def URL_TRANSFER(self):
        return self._URL_TRANSFER

    @property
    def URL_INGEST(self):
        return self._URL_INGEST

    # General path constants

    @property
    def WORKING_PATH(self):
        return self._WORKING_PATH

    @property
    def HANDLER_PATH(self):
        return self._HANDLER_PATH

    @property
    def SOURCE_PATH(self):
        return self._SOURCE_PATH

    @property
    def DONE_SOURCE_PATH(self):
        return self._DONE_SOURCE_PATH

    @property
    def FAILED_SOURCE_PATH(self):
        return self._FAILED_SOURCE_PATH

    # Processing path constants

    @property
    def PROCESS_PATH(self):
        return self._PROCESS_PATH

    @property
    def PROCESS_DEFAULT(self):
        return self._PROCESS_DEFAULT

    @property
    def PROCESS_AUTOMATED(self):
        return self._PROCESS_AUTOMATED

    @property
    def PROCESS_PATH_AUTOMATED(self):
        return self._PROCESS_PATH_AUTOMATED

    @property
    def PROCESS_PATH_DEFAULT(self):
        return self._PROCESS_PATH_DEFAULT

    @property
    def LOCAL_PROCESS_DIR(self):
        return self._LOCAL_PROCESS_DIR

    @property
    def DEBUG_FILE(self):
        return self._DEBUG_FILE

    @property
    def DEBUG_PATH(self):
        return self._DEBUG_PATH

    # Database constants

    @property
    def DB_FILE(self):
        return self._DB_FILE

    @property
    def CREATE_TRANSFER_TABLE(self):
        return self._CREATE_TRANSFER_TABLE

    @property
    def CREATE_SOURCE_TABLE(self):
        return self._CREATE_SOURCE_TABLE

    @property
    def DELETE_TRANSFER(self):
        return self._DELETE_TRANSFER

    @property
    def INSERT_TRANSFER(self):
        return self._INSERT_TRANSFER

    @property
    def UPDATE_STATUS_TRANSFER(self):
        return self._UPDATE_STATUS_TRANSFER

    @property
    def ALL_TRANSFERS(self):
        return self._ALL_TRANSFERS

    @property
    def ALL_NOT_COMPLETED_TRANSFERS(self):
        return self._ALL_NOT_COMPLETED_TRANSFERS

    @property
    def ALL_PROCESSING_TRANSFERS(self):
        return self._ALL_PROCESSING_TRANSFERS

    @property
    def ONE_TRANSFER_UUID(self):
        return self._ONE_TRANSFER_UUID

    @property
    def ONE_TRANSFER_SOURCE_ID(self):
        return self._ONE_TRANSFER_SOURCE_ID

    @property
    def ACTIVE_TRANSFERS(self):
        return self._ACTIVE_TRANSFERS

    @property
    def SELECT_SIP_UUID_TRANSFER(self):
        return self._SELECT_SIP_UUID_TRANSFER

    @property
    def UPDATE_SIP_UUID_TRANSFER(self):
        return self._UPDATE_SIP_UUID_TRANSFER

    @property
    def COUNT_FAILED_TRANSFER(self):
        return self._COUNT_FAILED_TRANSFER

    @property
    def DELETE_SOURCE(self):
        return self._DELETE_SOURCE

    @property
    def INSERT_SOURCE(self):
        return self._INSERT_SOURCE

    @property
    def UPDATE_STATUS_SOURCE(self):
        return self._UPDATE_STATUS_SOURCE

    @property
    def ALL_SOURCES(self):
        return self._ALL_SOURCES

    @property
    def ONE_SOURCE_NAME(self):
        return self._ONE_SOURCE_NAME

    @property
    def ONE_SOURCE_ID(self):
        return self._ONE_SOURCE_ID

    @property
    def UNSTARTED_SOURCE(self):
        return self._UNSTARTED_SOURCE

    # Miscellaneous constants

    @property
    def SOURCE(self):
        return self._SOURCE

    @property
    def TRANSFER(self):
        return self._TRANSFER

    @property
    def INGEST(self):
        return self._INGEST

    @property
    def GET_ALL(self):
        return self._GET_ALL

    @property
    def GET_ONE(self):
        return self._GET_ONE

    @property
    def GET_ACTIVE(self):
        return self._GET_ACTIVE

    @property
    def GET_UNSTARTED(self):
        return self._GET_UNSTARTED

    @property
    def INSERT(self):
        return self._INSERT

    @property
    def DELETE(self):
        return self._DELETE

    @property
    def FAILED(self):
        return self._FAILED

    @property
    def REJECTED(self):
        return self._REJECTED

    @property
    def USER_INPUT(self):
        return self._USER_INPUT

    @property
    def COMPLETE(self):
        return self._COMPLETE

    @property
    def PROCESSING(self):
        return self._PROCESSING

    @property
    def TYPE_TRANSFER(self):
        return self._TYPE_TRANSFER

    @property
    def TYPE_INGEST(self):
        return self._TYPE_INGEST

    @property
    def SOURCE_DICT(self):
        return self._SOURCE_DICT

    @property
    def STATUS_LIST(self):
        return self._STATUS_LIST
