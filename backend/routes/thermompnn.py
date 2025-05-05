import os
import logging
import uuid
import requests
import urllib.parse
from flask import Blueprint, request, jsonify
from backend.services.thermompnn_service import run_thermompnn
from backend.database.azure_upload import upload_task_outputs  # Azure upload function

# Define Blueprint
thermompnn_bp = Blueprint("thermompnn", __name__)

# Define Directories
UPLOAD_FOLDER = "/home/texsols/BioTasks/uploads"
OUTPUT_FOLDER = "/home/texsols/BioTasks/outputs/thermompnn_output"

# Ensure Directories Exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def download_file(url, save_path):
    """Download file from a URL to the specified path."""
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        logging.info(f"Successfully downloaded file from URL to {save_path}")
        return save_path
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download file from URL: {url} - {e}")
        raise Exception(f"Failed to download file from URL: {url} - {e}")


@thermompnn_bp.route("/predict", methods=["POST"])
def predict():
    """Starts ThermoMPNN and returns a task ID with Azure Blob Storage links."""
    try:
        task_type = request.form.get("task_type")  # 'single', 'epistatic', or 'double'
        pdb_file = request.files.get("pdb_file")
        pdb_file_url = request.form.get("pdb_file_url")

        if not pdb_file and not pdb_file_url:
            logging.error("No PDB file provided (upload or URL).")
            return jsonify({"error": "PDB file not provided (upload or URL)."}), 400

        # Generate unique task ID
        task_id = str(uuid.uuid4())

        # Handle PDB file from upload or URL
        if pdb_file:
            pdb_filepath = os.path.join(UPLOAD_FOLDER, f"{task_id}_{pdb_file.filename}")
            pdb_file.save(pdb_filepath)
            logging.info(f"PDB file uploaded: {pdb_filepath}")
        else:
            parsed_url = urllib.parse.urlparse(pdb_file_url)
            filename = os.path.basename(parsed_url.path)
            pdb_filepath = os.path.join(UPLOAD_FOLDER, f"{task_id}_{filename}")
            logging.info(f"Downloading PDB file from URL: {pdb_file_url}")
            download_file(pdb_file_url, pdb_filepath)

        # Prepare parameters
        params = {
            "task_type": task_type,
            "pdb_file": pdb_filepath,
            "task_id": task_id
        }

        logging.info(f"Starting ThermoMPNN with task ID: {task_id}, task type: {task_type}")
        result = run_thermompnn(params)

        return jsonify(result)

    except Exception as e:
        logging.error(f"Error in predict: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@thermompnn_bp.route("/check_status/<task_id>", methods=["GET"])
def check_status(task_id):
    """Check if ThermoMPNN has finished running and return Azure storage links."""
    try:
        task_folder = os.path.join(OUTPUT_FOLDER, task_id)
        log_file = os.path.join(task_folder, f"{task_id}.log")

        if not os.path.exists(log_file):
            logging.warning(f"Task ID {task_id} not found.")
            return jsonify({"error": "Task ID not found"}), 404

        with open(log_file, "r") as f:
            logs = f.readlines()

        azure_result = upload_task_outputs(task_id, task_folder)

        return jsonify({
            "task_id": task_id,
            "logs": logs,
            "azure_files": azure_result.get("uploaded_files", [])
        })

    except Exception as e:
        logging.error(f"Error in check_status: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
