import subprocess

from sysParameters import *


def compare_processing_file(procFile):
    diffPath = "bash " + HANDLER_PATH + LOCAL_PROCESS + "diffProcessing.sh " + HANDLER_PATH + LOCAL_PROCESS + procFile
    diff = subprocess.check_output(diffPath, shell=True)
    if len(diff) > 0:
        print("there is a diff")
        #TODO change processing file method
        return
    else:
        print("there is no diff")
        #TODO
        return
    return


def change_processing_file():
    pass


def choose_processing_file():
    pass
