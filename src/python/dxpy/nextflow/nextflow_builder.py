import os
from dxpy.nextflow.nextflow_templates import *
NF_PATH_LOCAL = ".dx_nextflow/"
DXAPP = "{}dxapp.json".format(NF_PATH_LOCAL)
EXEC = "{}src/nextflow.sh".format(NF_PATH_LOCAL)
DXAPP_CONTENT = get_nextflow_dxapp()

def write_exec():
    exec_content = get_nextflow_src()
    print(EXEC)
    print(exec_content)
    os.makedirs(os.path.dirname(os.path.abspath(EXEC)), exist_ok=True)
    with open(EXEC, "w") as exec:
        exec.write(exec_content)

def write_dxapp():
    with open(DXAPP, "w") as dxapp:
        dxapp.write(DXAPP_CONTENT)

def prepare_nextflow(args):
    if not os.path.exists(NF_PATH_LOCAL):
        os.makedirs(NF_PATH_LOCAL, exist_ok=True)
    write_dxapp()
    write_exec()
