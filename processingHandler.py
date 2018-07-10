import subprocess

from sysParameters import *


def compare_processing_file(procFile):
    diffPath = "bash " + HANDLER_PATH + LOCAL_PROCESS + "diffProcessing.sh " + HANDLER_PATH + LOCAL_PROCESS + procFile
    diff = subprocess.check_output(diffPath, shell=True)
    if len(diff) > 0:
        change_processing_file(procFile)
        return
    return


def change_processing_file(procFile):
    changePath = "bash " + HANDLER_PATH + LOCAL_PROCESS + "changeProcessing.sh " + HANDLER_PATH + LOCAL_PROCESS + procFile
    subprocess.check_output(changePath, shell=True)
    return
