import os
import subprocess
import logging
from backend.database.azure_upload import upload_task_outputs  # Azure upload function

# Paths and Constants
THERMOMPNN_SCRIPT = os.path.abspath("/home/texsols/BioTasks/tasks/ThermoMPNN-D/v2_ssm.py")
OUTPUT_FOLDER = os.path.abspath("/home/texsols/BioTasks/outputs/thermompnn_output")
UPLOAD_FOLDER = os.path.abspath("/home/texsols/BioTasks/uploads")
CONDA_ENV_NAME = "ThermoMPNN-D"  # Conda environment for ThermoMPNN

# Ensure output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_file_type(file_path):
    """Get the file type based on the extension."""
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == '.pdb':
        return 'pdb'
    elif ext == '.csv':
        return 'csv'
    elif ext == '.log':
        return 'log'
    else:
        return 'unknown'


def generate_azure_link(task_id, file_name):
    """Generate a dynamic Azure link for the output file."""
    base_url = "https://biotex.blob.core.windows.net/proteinfold/outputs/thermompnn_output"
    sas_token = "?sp=r&st=2025-04-24T18:49:42Z&se=2025-12-06T03:49:42Z&spr=https&sv=2024-11-04&sr=c&sig=DKTFbrdckeXxXPqxb0Nc%2Fn9vEz6lwR%2FudFYcj9XmugQ%3D"
    return f"{base_url}/{task_id}/{file_name}{sas_token}"


def run_thermompnn(params):
    """Runs ThermoMPNN for different task types (modes), uploads outputs to Azure, and returns task details."""
    task_id = params["task_id"]
    task_type = params["task_type"]  # 'single', 'additive', or 'epistatic'
    pdb_file = params["pdb_file"]
    
    task_output_folder = os.path.join(OUTPUT_FOLDER, task_id)
    os.makedirs(task_output_folder, exist_ok=True)

    # Define log file
    output_log = os.path.join(task_output_folder, f"{task_id}.log")

    # Set batch size based on task_type
    if task_type == "single":
        batch_size = 256
    elif task_type == "additive":
        batch_size = 256
    elif task_type == "epistatic":
        batch_size = 2048
    else:
        raise ValueError("Invalid task_type provided")

    # Build command
    command = f"""
    source ~/miniconda3/etc/profile.d/conda.sh &&
    conda activate {CONDA_ENV_NAME} &&
    python3 {THERMOMPNN_SCRIPT} \
        --mode {task_type} \
        --pdb "{pdb_file}" \
        --batch_size {batch_size} \
        --out "{task_output_folder}/ssm" \
        > "{output_log}" 2>&1
    """

    logging.info(f"Executing ThermoMPNN command:\n{command}")
    subprocess.run(command, shell=True, executable="/bin/bash")

    # Collect output files and their details
    output_files = [output_log, f"{task_output_folder}/ssm"]
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
        "message": "ThermoMPNN processing completed",
        "task_id": task_id,
        "azure_files": azure_result.get("uploaded_files", []),
        "output_log": azure_result.get("uploaded_files", [])[0] if azure_result.get("uploaded_files") else None,
        "output_file_details": file_info  # List of file names, types, and Azure links
    }
