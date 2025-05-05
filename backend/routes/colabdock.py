import os
import uuid
import logging
import requests
from flask import Blueprint, request, jsonify
from backend.services.colabdock_service import run_colabdock
from backend.database.azure_upload import upload_task_outputs

colabdock_bp = Blueprint("colabdock", __name__)

UPLOAD_FOLDER = "/home/texsols/BioTasks/uploads"
OUTPUT_FOLDER = "/home/texsols/BioTasks/outputs/colabdock_output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def download_file(url, save_path):
    """Download file from a URL to the specified path."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(response.content)
        logging.info(f"Successfully downloaded file from URL: {url}")
        return save_path
    except Exception as e:
        logging.error(f"Failed to download file from URL: {url} - {e}")
        raise Exception(f"Failed to download file from URL: {url} - {e}")


@colabdock_bp.route("/dock", methods=["POST"])
def dock():
    try:
        pdb_file = request.files.get("pdb_file")
        pdb_url = request.form.get("pdb_url")

        if not pdb_file and not pdb_url:
            logging.error("No PDB file or PDB URL provided")
            return jsonify({"error": "No PDB file or PDB URL provided"}), 400

        task_id = str(uuid.uuid4())

        # Handle PDB File
        if pdb_file:
            pdb_filepath = os.path.join(UPLOAD_FOLDER, f"{task_id}_{pdb_file.filename}")
            pdb_file.save(pdb_filepath)
        elif pdb_url:
            pdb_filename = f"{task_id}_pdb_from_url"
            pdb_filepath = os.path.join(UPLOAD_FOLDER, pdb_filename)
            download_file(pdb_url, pdb_filepath)

        # Prepare Parameters
        params = {
            "task_id": task_id,
            "pdb_file": pdb_filepath,
        }

        logging.info(f"Starting ColabDock task ID: {task_id}")
        result = run_colabdock(params)

        return jsonify(result)

    except Exception as e:
        logging.error(f"Error in dock: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@colabdock_bp.route("/check_status/<task_id>", methods=["GET"])
def check_status(task_id):
    try:
        task_folder = os.path.join(OUTPUT_FOLDER, task_id)
        log_file = os.path.join(task_folder, f"{task_id}.log")

        if not os.path.exists(log_file):
            logging.warning(f"Task ID {task_id} not found.")
            return jsonify({"error": "Task ID not found"}), 404

        # Read the log file (Optional)
        with open(log_file, "r") as f:
            logs = f.readlines()

        # Upload task outputs to Azure
        azure_result = upload_task_outputs(task_id, task_folder)

        return jsonify({
            "task_id": task_id,
            "logs": logs,
            "azure_files": azure_result.get("uploaded_files", [])
        })

    except Exception as e:
        logging.error(f"Error in check_status: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
