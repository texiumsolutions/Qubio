import os
import subprocess
import json
import uuid
import logging
from backend.database.azure_upload import upload_task_outputs  # Azure upload function

# Paths and Constants
TS_SCRIPT = "/home/texsols/BioTasks/tasks/TS/ts_main.py"
OUTPUT_FOLDER = "/home/texsols/BioTasks/outputs/ts_output"
TS_WORKING_DIR = "/home/texsols/BioTasks/tasks/TS"
CONDA_ENV_NAME = "ts_env"

# Default reagent files (absolute paths)
DEFAULT_REAGENTS = [
    os.path.join(TS_WORKING_DIR, "data/primary_amines_ok.smi"),
    os.path.join(TS_WORKING_DIR, "data/carboxylic_acids_ok.smi")
]

# Evaluator-specific arguments
EVALUATOR_ARGS = {
    "FPEvaluator": {"query_smiles": "COC(=O)[C@@H](O)CC(=O)Nc1nncc2ccccc12"},
    "MLClassifierEvaluator": {"model_filename": "mapk1_modl.pkl"},
    "FredEvaluator": {"design_unit_file": os.path.join(TS_WORKING_DIR, "data/2zdt_receptor.oedu")},
    "ROCSEvaluator": {"query_molfile": os.path.join(TS_WORKING_DIR, "data/2chw_lig.sdf")}
}

# Ensure output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_file_type(file_path):
    """Get the file type based on the extension."""
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == '.smi':
        return 'smi'
    elif ext == '.csv':
        return 'csv'
    elif ext == '.json':
        return 'json'
    elif ext == '.log':
        return 'log'
    else:
        return 'unknown'


def generate_azure_link(task_id, file_name):
    """Generate a dynamic Azure link for the output file."""
    base_url = "https://biotex.blob.core.windows.net/proteinfold/outputs/ts_output"
    sas_token = "?sp=r&st=2025-04-24T18:49:42Z&se=2025-12-06T03:49:42Z&spr=https&sv=2024-11-04&sr=c&sig=DKTFbrdckeXxXPqxb0Nc%2Fn9vEz6lwR%2FudFYcj9XmugQ%3D"
    return f"{base_url}/{task_id}/{file_name}{sas_token}"


def run_thompson_sampling(params):
    """Runs Thompson Sampling, uploads outputs to Azure, and returns task details."""

    # Generate unique task ID
    task_id = params["task_id"]
    task_output_folder = os.path.join(OUTPUT_FOLDER, task_id)
    os.makedirs(task_output_folder, exist_ok=True)  # Ensure task folder exists
    output_file = os.path.join(task_output_folder, f"{task_id}.csv")
    output_log = os.path.join(task_output_folder, f"{task_id}.log")
    json_path = os.path.join(task_output_folder, f"{task_id}.json")

    # Set evaluator args dynamically
    evaluator = params["evaluator"]
    evaluator_arg = params.get("evaluator_arg", EVALUATOR_ARGS.get(evaluator, {}))

    # Prepare the JSON config file
    json_config = {
        "reagent_file_list": params.get("reagent_file_list", DEFAULT_REAGENTS),
        "reaction_smarts": params["reaction_smarts"],
        "num_warmup_trials": params["num_warmup_trials"],
        "num_ts_iterations": params["num_ts_iterations"],
        "evaluator_class_name": evaluator,
        "evaluator_arg": evaluator_arg,
        "ts_mode": params["ts_mode"],
        "log_filename": output_log,
        "results_filename": output_file
    }

    # Save the config JSON file
    with open(json_path, "w") as f:
        json.dump(json_config, f, indent=4)

    # Construct the execution command
    command = f"""
    cd {TS_WORKING_DIR} &&
    source ~/miniconda3/etc/profile.d/conda.sh && conda activate {CONDA_ENV_NAME} &&
    python3 {TS_SCRIPT} {json_path} > "{output_log}" 2>&1
    """

    logging.info(f"Executing Thompson Sampling command:\n{command}")
    subprocess.run(command, shell=True, executable="/bin/bash", cwd=TS_WORKING_DIR)

    # Collect output files and their details
    output_files = [output_log, output_file, json_path]
    file_info = []

    # Walk through the output folder and gather file details
    for root, dirs, files in os.walk(task_output_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_type = get_file_type(file_path)
            azure_link = generate_azure_link(task_id, file_name)
            file_info.append({
                "file_name": file_name,
                "file_type": file_type,
                "azure_link": azure_link
            })

    # Upload task outputs to Azure
    azure_result = upload_task_outputs(task_id, task_output_folder)

    return {
        "message": "Thompson Sampling processing completed",
        "task_id": task_id,
        "azure_files": azure_result.get("uploaded_files", []),
        "output_log": azure_result.get("uploaded_files", [])[0] if azure_result.get("uploaded_files") else None,
        "output_file_details": file_info  # List of file names, types, and Azure links
    }

