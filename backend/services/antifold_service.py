import os
import subprocess
import logging
import uuid
from backend.database.azure_upload import upload_task_outputs  # Azure upload function

# Paths and Constants
ANTIFOLD_SCRIPT = os.path.abspath("/home/texsols/BioTasks/tasks/AntiFold/antifold/main.py")
OUTPUT_FOLDER = os.path.abspath("/home/texsols/BioTasks/outputs/antifold_output")
UPLOAD_FOLDER = os.path.abspath("/home/texsols/BioTasks/uploads")
CONDA_ENV_NAME = "antifold_cpu"

# Ensure output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def extract_chain_ids(pdb_file):
    """Extract unique chain IDs from a PDB file."""
    with open(pdb_file, "r") as f:
        chains = set(line.split()[4] for line in f if line.startswith("ATOM"))
    return list(chains)


def get_file_type(file_path):
    """Get the file type based on extension."""
    ext = os.path.splitext(file_path)[-1].lower()
    
    if ext == '.csv':
        return 'csv'
    elif ext == '.txt':
        return 'txt'
    elif ext == '.pdb':
        return 'pdb'
    elif ext == '.log':
        return 'log'
    else:
        return 'unknown'  # Default if not recognized


def generate_azure_link(task_id, file_name):
    """Generate a dynamic Azure link for the output file."""
    base_url = "https://biotex.blob.core.windows.net/proteinfold/outputs/antifold_output"
    sas_token = "?sp=r&st=2025-04-24T18:49:42Z&se=2025-12-06T03:49:42Z&spr=https&sv=2024-11-04&sr=c&sig=DKTFbrdckeXxXPqxb0Nc%2Fn9vEz6lwR%2FudFYcj9XmugQ%3D"
    return f"{base_url}/{task_id}/{file_name}{sas_token}"


def run_antifold(params):
    """Runs AntiFold, sets correct --out_dir, uploads outputs to Azure, and returns task details."""
    task_id = params["task_id"]
    task_output_folder = os.path.join(OUTPUT_FOLDER, task_id)
    os.makedirs(task_output_folder, exist_ok=True)  # Ensure output folder exists

    # Define log file
    output_log = os.path.join(task_output_folder, f"{task_id}.log")

    # Construct the command with --out_dir
    command = f"""
    source ~/miniconda3/etc/profile.d/conda.sh &&
    conda activate {CONDA_ENV_NAME} &&
    python3 {ANTIFOLD_SCRIPT} \
        --out_dir "{task_output_folder}" \
        --pdb_file "{params['pdb_file']}" \
        --heavy_chain "{params['heavy_chain']}" \
        --light_chain "{params['light_chain']}" \
        > "{output_log}" 2>&1
    """

    logging.info(f"Executing AntiFold command:\n{command}")
    subprocess.run(command, shell=True, executable="/bin/bash")
    
    # Get the generated output file(s)
    output_files = [f for f in os.listdir(task_output_folder) if os.path.isfile(os.path.join(task_output_folder, f))]
    file_info = []

    # Check each output file, determine its type, and create a file info entry
    for output_file in output_files:
        output_file_path = os.path.join(task_output_folder, output_file)
        file_type = get_file_type(output_file_path)
        azure_link = generate_azure_link(task_id, output_file)  # Generate dynamic Azure link
        file_info.append({
            "file_name": output_file,
            "file_type": file_type,
            "azure_link": azure_link
        })

    # Upload task outputs to Azure
    azure_result = upload_task_outputs(task_id, task_output_folder)

    return {
        "message": "AntiFold processing completed",
        "task_id": task_id,
        "azure_files": azure_result.get("uploaded_files", []),
        "output_log": azure_result.get("uploaded_files", [])[0] if azure_result.get("uploaded_files") else None,
        "output_file_details": file_info  # List of file names, types, and Azure links
    }
