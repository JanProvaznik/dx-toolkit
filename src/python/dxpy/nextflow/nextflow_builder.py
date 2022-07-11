import os
from dxpy.nextflow.nextflow_templates import *
import tempfile
import dxpy
DXAPP_CONTENT = get_nextflow_dxapp()


def write_exec(folder):
    exec_file = f"{folder}/nextflow.sh"
    exec_content = get_nextflow_src()
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
def build_pipeline_from_repository(args=None):
    build_project_id = dxpy.WORKSPACE_ID
    if build_project_id is None:
        parser.error("Can't create an applet without specifying a destination project; please use the -d/--destination flag to explicitly specify a project")
    input_hash = {
        "repository_url": args.repository,
    }

    api_options = {
        "name": "Nextflow build of %s" % (args.repository),
        "input": input_hash,
        "project": build_project_id,
    }
    # TODO: this will have to be an app app_run!
    app_run_result = dxpy.api.applet_run('applet-GF62KQj0k25f4v1Z7KgkFFKx', input_params=api_options)
    job_id = app_run_result["id"]
    print("Started builder job %s" % (job_id,))
    dxpy.DXJob(job_id).wait_on_done(interval=1)
    applet_id, _ = dxpy.get_dxlink_ids(dxpy.api.job_describe(job_id)['output']['output_applet'])
    return applet_id
    # subprocess.check_call(
    #     ['dx', 'run', 'applet-GF419100k25ZQXKQ972V4G00', f'-irepository_url={args.repository}', '--brief', '--priority',
    #      'high', '-y'])

    ...

def prepare_nextflow(args=None) -> str:
    dxapp_dir = tempfile.mkdtemp(prefix="dx.nextflow.")
    write_dxapp(dxapp_dir)
    write_exec(dxapp_dir)

    return dxapp_dir
