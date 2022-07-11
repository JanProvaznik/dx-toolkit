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
        {
            "name": "nf_run_args_and_pipeline_params",
            "label": "Nextflow Run Arguments and Pipeline Parameters",
            "help": "Additional run arguments and pipeline parameters for Nextflow (i.e. -queue-size).",
            "class": "string",
            "optional": true
        },
        {
            "name": "resume",
            "label": "Resume",
            "help": "Enables resume functionality in Nextflow workflows.",
            "class": "boolean",
            "default": false
        },
        {
            "name": "resume_session",
            "label": "Resume Session",
            "help": "Session or job to be resumed.",
            "class": "string",
            "optional": true
        },
        {
            "name": "nf_advanced_opts",
            "label": "Nextflow Advanced Options",
            "help": "Advanced options for Nextflow (i.e. -quiet).",
            "class": "string",
            "optional": true
        },
        {
            "name": "docker_creds",
            "label": "Docker Credentials",
            "help": "Docker Credentials used to obtain private docker images.",
            "class": "file",
            "optional": true
        },
        {
            "name": "debug",
            "label": "Debug Mode",
            "help": "Shows additional information in Nextflow logs.",
            "class": "boolean",
            "default": false
        },
        {
            "name": "secret_directive_file",
            "label": "Secret Directive File",
            "help": "Adds the built-in Nextflow support for pipeline secrets to allow users to handle and manage sensitive information for pipeline execution in a safe manner.",
            "class": "file",
            "optional": true
        },
        {
            "name": "no_future_resume",
            "label": "No Future Resume",
            "help": "Allow saving workspace and cache files to the platform to be used later for resume functionality.",
            "class": "boolean",
            "default": false
        }
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
    }'''


def get_nextflow_src():
    return '''
    #!/usr/bin/env bash
    curl -s https://get.nextflow.io | bash
    mv nextflow /usr/bin
    nextflow run /
    '''
