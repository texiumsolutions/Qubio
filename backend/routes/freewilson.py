import os
import logging
import uuid
import requests
from flask import Blueprint, request, jsonify
from backend.services.freewilson_service import run_freewilson
from backend.database.azure_upload import upload_task_outputs  # Azure upload function

# Define Blueprint
freewilson_bp = Blueprint("freewilson", __name__)

# Define Directories
UPLOAD_FOLDER = "/home/texsols/BioTasks/uploads"
OUTPUT_FOLDER = "/home/texsols/BioTasks/outputs/freewilson_output"

# Ensure Directories Exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Configure Logging
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


@freewilson_bp.route("/run_analysis", methods=["POST"])
def run_analysis():
    """Runs Free-Wilson analysis and returns a task ID with Azure Blob Storage links."""
    try:
        scaffold_file = request.files.get("scaffold_file")
        input_smiles_file = request.files.get("input_smiles_file")
        activity_file = request.files.get("activity_file")

        scaffold_url = request.form.get("scaffold_url")
        input_smiles_url = request.form.get("input_smiles_url")
        activity_url = request.form.get("activity_url")

        job_prefix = request.form.get("prefix", str(uuid.uuid4()))  # Default: random UUID

        # Validate Required Files or URLs
        if not scaffold_file and not scaffold_url:
            logging.error("Missing scaffold file or scaffold URL")
            return jsonify({"error": "Missing scaffold file or scaffold URL"}), 400
        if not input_smiles_file and not input_smiles_url:
            logging.error("Missing SMILES file or SMILES URL")
            return jsonify({"error": "Missing SMILES file or SMILES URL"}), 400
        if not activity_file and not activity_url:
            logging.error("Missing activity file or activity URL")
            return jsonify({"error": "Missing activity file or activity URL"}), 400

        # Generate unique task ID
        task_id = str(uuid.uuid4())

        # Handle Scaffold File
        if scaffold_file:
            scaffold_filepath = os.path.join(UPLOAD_FOLDER, f"{task_id}_{scaffold_file.filename}")
            scaffold_file.save(scaffold_filepath)
        elif scaffold_url:
            scaffold_filename = f"{task_id}_scaffold_from_url"
            scaffold_filepath = os.path.join(UPLOAD_FOLDER, scaffold_filename)
            download_file(scaffold_url, scaffold_filepath)

        # Handle SMILES File
        if input_smiles_file:
            input_smiles_filepath = os.path.join(UPLOAD_FOLDER, f"{task_id}_{input_smiles_file.filename}")
            input_smiles_file.save(input_smiles_filepath)
        elif input_smiles_url:
            input_smiles_filename = f"{task_id}_smiles_from_url"
            input_smiles_filepath = os.path.join(UPLOAD_FOLDER, input_smiles_filename)
            download_file(input_smiles_url, input_smiles_filepath)

        # Handle Activity File
        if activity_file:
            activity_filepath = os.path.join(UPLOAD_FOLDER, f"{task_id}_{activity_file.filename}")
            activity_file.save(activity_filepath)
        elif activity_url:
            activity_filename = f"{task_id}_activity_from_url"
            activity_filepath = os.path.join(UPLOAD_FOLDER, activity_filename)
            download_file(activity_url, activity_filepath)

        # Prepare Parameters
        params = {
            "scaffold": scaffold_filepath,
            "input_smiles": input_smiles_filepath,
            "activity": activity_filepath,
            "prefix": job_prefix,
            "smarts": request.form.get("smarts", ""),
            "max_spec": request.form.get("max", ""),
            "log": request.form.get("log", "false").lower() == "true"
        }

        # Log and Run Free-Wilson
        logging.info(f"Starting Free-Wilson analysis with task ID: {job_prefix}")
        result = run_freewilson(params)

        return jsonify(result)

    except Exception as e:
        logging.error(f"Error in run_analysis: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@freewilson_bp.route("/check_status/<task_id>", methods=["GET"])
def check_status(task_id):
    """Check if Free-Wilson has finished running and return Azure storage links."""
    try:
        task_folder = os.path.join(OUTPUT_FOLDER, task_id)
        log_file = os.path.join(task_folder, f"{task_id}.log")

        if not os.path.exists(log_file):
            logging.warning(f"Task ID {task_id} not found.")
            return jsonify({"error": "Task ID not found"}), 404

        # Read the local log file (Optional)
        with open(log_file, "r") as f:
            logs = f.readlines()

        # Get Azure Blob Storage links
        azure_result = upload_task_outputs(task_id, task_folder)

        return jsonify({
            "task_id": task_id,
            "logs": logs,
            "azure_files": azure_result.get("uploaded_files", [])
        })

    except Exception as e:
        logging.error(f"Error in check_status: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
