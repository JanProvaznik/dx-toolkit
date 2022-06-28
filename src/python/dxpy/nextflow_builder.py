import os

NF_PATH_LOCAL = ".dx_nextflow/"
DXAPP = ".dx_nextflow/dxapp.json"
DXAPP_CONTENT = '''
{
  "name": "nextflow",
  "title": "nextflow",
  "summary": "nextflow",
  "dxapi": "1.0.0",
  "openSource": true,
  "billTo": "org-dnanexus_apps",
  "version": "1.0.0",
  "inputSpec": [
  ],
  "outputSpec": [
  ],
  "runSpec": {
    "interpreter": "bash",
    "execDepends": [
      {
        "name": "default-jre"
      }
    ],
    "distribution": "Ubuntu",
    "release": "20.04",
    "file": "nextflow.sh",
    "version": "0"
  },
  "regionalOptions": {
    "aws:us-east-1": {
      "systemRequirements": {
        "*": {
          "instanceType": "mem1_ssd1_v2_x8"
        }
      }
    }
  },
  "details": {
    "whatsNew": "1.0.0: initial version"
  },
  "categories": [],
  "access": {
    "network": [
      "*"
    ],
    "project": "CONTRIBUTE",
    "allProjects": "VIEW"
  }
}
'''

def write_exec(repo, tag):
    GCLONE_PLACEHOLDER = "@GIT_CLONE_PLACEHOLDER"
    GCHECKOUT_PLACEHOLDER = "@GIT_CHECKOUT_PLACEHOLDER"
    EXEC = ".dx_nextflow/nextflow.sh"
    exec_content = f'''
        #!/usr/bin/env bash
        curl -s https://get.nextflow.io | bash
        mv nextflow /usr/bin
        {GCLONE_PLACEHOLDER}
        {GCHECKOUT_PLACEHOLDER}
        nextflow run /
    '''
    g_clone = ""
    g_checkout = ""
    if repo:
        g_clone = f"git clone {repo} /"
        if tag:
            g_checkout = f'''
            pushd /
            git checkout {tag}
            popd
            '''
    exec_content=exec_content.replace(GCLONE_PLACEHOLDER, g_clone).replace(GCHECKOUT_PLACEHOLDER, g_checkout)

    with open(EXEC, "w") as exec:
        exec.write(exec_content)

def write_dxapp():
    with open(DXAPP, "w") as dxapp:
        dxapp.write(DXAPP_CONTENT)

def prepare_nextflow(args):
    if not os.path.exists(NF_PATH_LOCAL):
        os.makedirs(NF_PATH_LOCAL)
    write_dxapp()
    write_exec(args._repository, args._tag)
