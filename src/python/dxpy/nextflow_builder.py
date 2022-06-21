import os

NF_PATH_LOCAL = ".dx_nextflow/"
DXAPP = ".dx_nextflow/dxapp.json"
EXEC = ".dx_nextflow/nextflow.sh"
EXEC_CONTENT = '''
# #!/usr/bin/env bash
curl -s "https://get.nextflow.io" | bash
mv nextflow /usr/bin

nextflow run /
'''
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
    "interpreter": "python3",
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
  },
  "ignoreReuse": true
}
'''
def prepare_nextflow():
    print("here")
    if not os.path.exists(NF_PATH_LOCAL):
        os.makedirs(NF_PATH_LOCAL)
    print("here2")
    with open(DXAPP, "w") as dxapp:
        dxapp.write(DXAPP_CONTENT)
    print("here3")
    with open(EXEC, "w") as exec:
        exec.write(EXEC_CONTENT)
    print("here4")