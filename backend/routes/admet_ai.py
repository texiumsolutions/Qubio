import os
import logging
import uuid
from flask import Blueprint, request, jsonify
from backend.services.admet_ai_service import run_admet_ai
from backend.database.azure_upload import upload_task_outputs

# Define Blueprint
admet_bp = Blueprint("admet_ai", __name__)

# Directories
UPLOAD_FOLDER = "/home/texsols/BioTasks/uploads"
OUTPUT_FOLDER = "/home/texsols/BioTasks/outputs/admet_ai_output"

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@admet_bp.route("/predict_admet", methods=["POST"])
def predict_admet():
    try:
        smiles_file = request.files.get("smiles_file")
        if not smiles_file:
            return jsonify({"error": "No SMILES file provided"}), 400

        task_id = str(uuid.uuid4())
        smiles_filename = f"{task_id}_{smiles_file.filename}"
        smiles_path = os.path.join(UPLOAD_FOLDER, smiles_filename)
        smiles_file.save(smiles_path)

        logging.info(f"SMILES file uploaded: {smiles_path}")

        # Run ADMET AI
        params = {
            "task_id": task_id,
            "smiles_file": smiles_path
        }

        result = run_admet_ai(params)
        return jsonify(result)

    except Exception as e:
        logging.error(f"ADMET AI prediction error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@admet_bp.route("/check_admet_status/<task_id>", methods=["GET"])
def check_admet_status(task_id):
    try:
        task_folder = os.path.join(OUTPUT_FOLDER, task_id)
        log_file = os.path.join(task_folder, f"{task_id}.log")

        if not os.path.exists(log_file):
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
        logging.error(f"Error checking ADMET AI status: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
