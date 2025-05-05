import os
import logging
import uuid
from flask import Blueprint, request, jsonify
from backend.services.thompson_sampling_service import run_thompson_sampling
from backend.database.azure_upload import upload_task_outputs  # Azure upload function

# Define Blueprint
ts_bp = Blueprint("thompson_sampling", __name__)

# Define Directories
OUTPUT_FOLDER = "/home/texsols/BioTasks/outputs/ts_output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@ts_bp.route("/run_ts", methods=["POST"])
def run_ts():
    """Starts Thompson Sampling and returns a task ID with Azure Blob Storage links."""
    try:
        # Retrieve form data
        data = request.form.to_dict()  # Convert ImmutableMultiDict to a regular dictionary

        required_params = [
            "reaction_smarts", "num_warmup_trials", "num_ts_iterations",
            "evaluator", "ts_mode"
        ]
        for param in required_params:
            if param not in data:
                logging.error(f"Missing required parameter: {param}")
                return jsonify({"error": f"Missing required parameter: {param}"}), 400

        if data["evaluator"] not in [
            "FPEvaluator", "MLClassifierEvaluator", "FredEvaluator", "ROCSEvaluator"
        ]:
            logging.error(f"Invalid evaluator selected: {data['evaluator']}")
            return jsonify({"error": "Invalid evaluator selected"}), 400

        # Convert numeric fields to integers
        try:
            data["num_warmup_trials"] = int(data["num_warmup_trials"])
            data["num_ts_iterations"] = int(data["num_ts_iterations"])
        except ValueError:
            logging.error(f"Invalid number format for warmup or iterations: {data['num_warmup_trials']}, {data['num_ts_iterations']}")
            return jsonify({"error": "Invalid number format for warmup or iterations"}), 400

        # Generate unique task ID
        task_id = str(uuid.uuid4())
        data["task_id"] = task_id  # Add task ID to data

        # Log and Run Thompson Sampling
        logging.info(f"Starting Thompson Sampling with task ID: {task_id}")
        result = run_thompson_sampling(data)

        return jsonify(result)

    except Exception as e:
        logging.error(f"Error in run_ts: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500



@ts_bp.route("/check_status/<task_id>", methods=["GET"])
def check_status(task_id):
    """Check if Thompson Sampling has completed and return logs along with Azure file links."""
    try:
        task_folder = os.path.join(OUTPUT_FOLDER, task_id)
        log_file = os.path.join(task_folder, f"{task_id}.log")

        if not os.path.exists(log_file):
            logging.warning(f"Task ID {task_id} not found.")
            return jsonify({"error": "Task ID not found"}), 404

        # Read log file (Optional)
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
