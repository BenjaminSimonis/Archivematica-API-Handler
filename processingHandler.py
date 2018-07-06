import subprocess

from sysParameters import *


def compare_processing_file(procFile):
    diffPath = "bash " + HANDLER_PATH + LOCAL_PROCESS + "/diffProcessing.sh " + procFile
    diff = subprocess.check_output(diffPath, shell=True)
    if len(diff) > 1:
        #TODO change processing file method
        pass
    else:
        #TODO
    pass


def change_processing_file():
    pass


def choose_processing_file():
    pass
