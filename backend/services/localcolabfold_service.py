import os
import subprocess
import logging
from backend.database.azure_upload import upload_task_outputs

# Paths and constants
COLABFOLD_CMD = "colabfold_batch"
OUTPUT_FOLDER = "/home/texsols/BioTasks/outputs/localcolabfold_output"
CONDA_ENV_PATH = "/home/texsols/BioTasks/tasks/localcolabfold/localcolabfold/colabfold-conda"

# Setup

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_localcolabfold(fasta_path, task_id):
    task_output_dir = os.path.join(OUTPUT_FOLDER, task_id)
    os.makedirs(task_output_dir, exist_ok=True)
    output_log = os.path.join(task_output_dir, f"{task_id}.log")

    command = f"""
    source ~/miniconda3/etc/profile.d/conda.sh &&
    conda activate {CONDA_ENV_PATH} &&
    {COLABFOLD_CMD} "{fasta_path}" "{task_output_dir}" > "{output_log}" 2>&1
    """

    logging.info(f"Running LocalColabFold for task ID {task_id}:\n{command}")
    subprocess.run(command, shell=True, executable="/bin/bash")

    uploaded = upload_task_outputs(task_id, task_output_dir)

    return {
        "message": "LocalColabFold prediction complete",
        "task_id": task_id,
        "azure_files": uploaded.get("uploaded_files", [])
    }
