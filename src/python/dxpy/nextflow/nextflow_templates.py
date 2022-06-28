def get_nextflow_dxapp():
    return '''
    {
        "name": "nextflow pipeline",
        "title": "Nextflow Pipeline",
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
            "file": "src/nextflow.sh",
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
    }'''

def get_nextflow_src():
    return '''
    #!/usr/bin/env bash
    curl -s https://get.nextflow.io | bash
    mv nextflow /usr/bin
    nextflow run /
    '''