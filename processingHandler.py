import subprocess

from sysParameters import *


def compare_processing_file(procFile):
    diffPath = "bash " + HANDLER_PATH + LOCAL_PROCESS + "diffProcessing.sh " + procFile
    diff = subprocess.check_output(diffPath, shell=True)
    print(len(diff))
    if len(diff) > 1:
        print("there is a diff")
        #TODO change processing file method
        pass
    else:
        print("there is no diff")
        #TODO
        pass
    pass


def change_processing_file():
    pass


def choose_processing_file():
    pass
