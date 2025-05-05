import os
import logging
import uuid
from flask import Blueprint, request, jsonify
from backend.services.reinvent_service import run_reinvent
from backend.database.azure_upload import upload_task_outputs

reinvent_bp = Blueprint("reinvent", __name__)

UPLOAD_FOLDER = "/home/texsols/BioTasks/uploads"
OUTPUT_FOLDER = "/home/texsols/BioTasks/outputs/reinvent_output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@reinvent_bp.route("/predict", methods=["POST"])
def predict():
    try:
        task_id = str(uuid.uuid4())
        smiles = request.form.get("smiles")

        if not smiles:
            return jsonify({"error": "SMILES input is required"}), 400

        params = {
            "smiles": smiles,
            "task_id": task_id,
        }

        logging.info(f"Starting REINVENT task ID: {task_id}")
        result = run_reinvent(params)

        return jsonify(result)

    except Exception as e:
        logging.error(f"Error in REINVENT predict: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@reinvent_bp.route("/check_status/<task_id>", methods=["GET"])
def check_status(task_id):
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
        logging.error(f"Error in check_status: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
