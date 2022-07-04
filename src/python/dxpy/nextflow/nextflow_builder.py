import os
from dxpy.nextflow.nextflow_templates import *
import tempfile

DXAPP_CONTENT = get_nextflow_dxapp()


def write_exec(folder):
    exec_file = f"{folder}/nextflow.sh"
    exec_content = get_nextflow_src()
    print(exec_file)
    print(exec_content)
    os.makedirs(os.path.dirname(os.path.abspath(exec_file)), exist_ok=True)
    with open(exec_file, "w") as exec:
        exec.write(exec_content)


def write_dxapp(folder):
    dxapp_file = f"{folder}/dxapp.json"
    with open(dxapp_file, "w") as dxapp:
        dxapp.write(DXAPP_CONTENT)


'''
Creates files needed for nextflow applet build and returns folder with these files.
Note that folder is created as a tempfile
'''


def prepare_nextflow(args=None) -> str:
    dxapp_dir = tempfile.mkdtemp(prefix="dx.nextflow.")
    write_dxapp(dxapp_dir)
    write_exec(dxapp_dir)

    return dxapp_dir
