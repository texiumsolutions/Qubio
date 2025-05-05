import os
import subprocess
import logging

from backend.database.azure_upload import upload_task_outputs

ADMET_SCRIPT = os.path.abspath("/home/texsols/BioTasks/tasks/admet_ai/admet_ai/admet_predict.py")
OUTPUT_FOLDER = os.path.abspath("/home/texsols/BioTasks/outputs/admet_ai_output")
CONDA_ENV_NAME = "admet_ai"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_file_type(file_path):
    """Get the file type based on the extension."""
    ext = os.path.splitext(file_path)[-1].lower()
    
    if ext == '.csv':
        return 'csv'
    elif ext == '.txt':
        return 'txt'
    elif ext == '.log':
        return 'log'
    else:
        return 'unknown'  # Default if not recognized


def generate_azure_link(task_id, file_name):
    """Generate a dynamic Azure link for the output file."""
    base_url = "https://biotex.blob.core.windows.net/proteinfold/outputs/admet_ai_output"
    sas_token = "?sp=r&st=2025-04-24T18:49:42Z&se=2025-12-06T03:49:42Z&spr=https&sv=2024-11-04&sr=c&sig=DKTFbrdckeXxXPqxb0Nc%2Fn9vEz6lwR%2FudFYcj9XmugQ%3D"
    return f"{base_url}/{task_id}/{file_name}{sas_token}"


def run_admet_ai(params):
    task_id = params["task_id"]
    smiles_file = params["smiles_file"]
    task_output_folder = os.path.join(OUTPUT_FOLDER, task_id)
    os.makedirs(task_output_folder, exist_ok=True)

    output_file = os.path.join(task_output_folder, "predictions.csv")
    log_file = os.path.join(task_output_folder, f"{task_id}.log")

    command = f"""
    source ~/miniconda3/etc/profile.d/conda.sh &&
    conda activate {CONDA_ENV_NAME} &&
    admet_predict --data_path "{smiles_file}" --save_path "{output_file}" --smiles_column smiles \
    > "{log_file}" 2>&1
    """

    logging.info(f"Running ADMET prediction:\n{command}")
    subprocess.run(command, shell=True, executable="/bin/bash")

    # Collect output files and their details
    output_files = [output_file, log_file]  # Add other files here if needed
    file_info = []

    for output_file in output_files:
        file_name = os.path.basename(output_file)
        file_type = get_file_type(output_file)
        azure_link = generate_azure_link(task_id, file_name)  # Generate dynamic Azure link
        file_info.append({
            "file_name": file_name,
            "file_type": file_type,
            "azure_link": azure_link
        })

    # Upload task outputs to Azure
    azure_result = upload_task_outputs(task_id, task_output_folder)

    return {
        "message": "ADMET AI prediction completed",
        "task_id": task_id,
        "azure_files": azure_result.get("uploaded_files", []),
        "output_log": azure_result.get("uploaded_files", [])[0] if azure_result.get("uploaded_files") else None,
        "output_file_details": file_info  # List of file names, types, and Azure links
    }
