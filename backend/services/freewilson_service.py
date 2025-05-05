import os
import subprocess
import logging
import uuid
from backend.database.azure_upload import upload_task_outputs  # Import Azure upload function

# Paths and Constants
FREE_WILSON_SCRIPT = os.path.abspath("/home/texsols/BioTasks/tasks/Free-Wilson/free_wilson.py")
OUTPUT_FOLDER = os.path.abspath("/home/texsols/BioTasks/outputs/freewilson_output")
UPLOAD_FOLDER = os.path.abspath("/home/texsols/BioTasks/uploads")
CONDA_ENV_NAME = "freewilson_env"

# Ensure output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_file_type(file_path):
    """Get the file type based on the extension."""
    ext = os.path.splitext(file_path)[-1].lower()
    
    if ext == '.pdb':
        return 'pdb'
    elif ext == '.log':
        return 'log'
    elif ext == '.txt':
        return 'txt'
    elif ext == '.csv':
        return 'csv'
    else:
        return 'unknown'

def generate_azure_link(task_id, file_name):
    """Generate a dynamic Azure link for the output file."""
    base_url = "https://biotex.blob.core.windows.net/proteinfold/outputs/freewilson_output"
    sas_token = "?sp=r&st=2025-04-24T18:49:42Z&se=2025-12-06T03:49:42Z&spr=https&sv=2024-11-04&sr=c&sig=DKTFbrdckeXxXPqxb0Nc%2Fn9vEz6lwR%2FudFYcj9XmugQ%3D"
    return f"{base_url}/{task_id}/{file_name}{sas_token}"

def run_freewilson(params):
    """Runs Free-Wilson, uploads outputs to Azure, and returns task details."""

    # Generate a unique task ID
    task_id = str(uuid.uuid4())
    task_output_folder = os.path.join(OUTPUT_FOLDER, task_id)
    os.makedirs(task_output_folder, exist_ok=True)  # Ensure directory exists
    output_log = os.path.join(task_output_folder, f"{task_id}.log")

    # Ensure all file paths are absolute
    scaffold_path = os.path.abspath(params["scaffold"])
    input_smiles_path = os.path.abspath(params["input_smiles"])
    activity_path = os.path.abspath(params["activity"])

    # Construct command
    max_spec = params.get("max_spec", "")
    max_arg = f'--max "{max_spec}"' if "|" in max_spec else ""
    smarts_arg = f'--smarts "{params["smarts"]}"' if params["smarts"] else ""

    command = f"""
    source ~/miniconda3/etc/profile.d/conda.sh &&
    conda activate {CONDA_ENV_NAME} &&
    python3 {FREE_WILSON_SCRIPT} all \
        --scaffold "{scaffold_path}" \
        --in "{input_smiles_path}" \
        --act "{activity_path}" \
        --prefix "{task_output_folder}/output" \
        {smarts_arg} \
        {max_arg} \
        {f'--log' if params["log"] else ""} \
        > "{output_log}" 2>&1
    """

    logging.info(f"Executing Free-Wilson command:\n{command}")
    subprocess.run(command, shell=True, executable="/bin/bash")

    # Collect output files and their details
    output_files = [output_log]  # Add any additional files generated during the process here if needed
    file_info = []

    # Assuming results are in the task_output_folder
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

    # Upload task outputs to Azure Blob Storage
    azure_result = upload_task_outputs(task_id, task_output_folder)

    return {
        "message": "Free-Wilson analysis completed",
        "task_id": task_id,
        "azure_files": azure_result.get("uploaded_files", []),
        "output_log": azure_result.get("uploaded_files", [])[0] if azure_result.get("uploaded_files") else None,
        "output_file_details": file_info  # List of file names, types, and Azure links
    }
