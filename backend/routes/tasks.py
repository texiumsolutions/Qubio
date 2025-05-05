from flask import Blueprint, jsonify
import datetime

# Define Blueprint
tasks_bp = Blueprint("tasks", __name__)

# Define Available Tasks
TASKS = [
    # AntiFold
    {"task": "AntiFold Prediction", "endpoint": "/v1/api/antifold/predict", "description": "Predicts protein structures using AntiFold."},
    {"task": "Check AntiFold Status", "endpoint": "/v1/api/antifold/check_status/<task_id>", "description": "Checks the prediction status of AntiFold."},

    # ProteinMPNN
    {"task": "ProteinMPNN ddG Prediction", "endpoint": "/v1/api/proteinmpnn/ddg", "description": "Predicts stability or binding affinity changes for mutations."},
    {"task": "Check ProteinMPNN Status", "endpoint": "/v1/api/proteinmpnn/check_status/<task_id>", "description": "Checks the processing status of ProteinMPNN."},

    # Thompson Sampling
    {"task": "Run Thompson Sampling", "endpoint": "/v1/api/thompson_sampling/run_ts", "description": "Performs Thompson Sampling for reaction optimization."},
    {"task": "Check Thompson Sampling Status", "endpoint": "/v1/api/thompson_sampling/check_status/<task_id>", "description": "Checks the status of a Thompson Sampling task."},

    # Free-Wilson, LigandMPNN)
    {"task": "Run Free-Wilson Analysis", "endpoint": "/v1/api/freewilson/run_fw", "description": "Runs Free-Wilson analysis for molecular property prediction."},
    {"task": "Check Free-Wilson Status", "endpoint": "/v1/api/freewilson/check_status/<task_id>", "description": "Checks Free-Wilson analysis task status."},

    {"task": "Run LigandMPNN", "endpoint": "/v1/api/ligandmpnn/run_lmpnn", "description": "Generates ligand mutations using LigandMPNN."},
    {"task": "Check LigandMPNN Status", "endpoint": "/v1/api/ligandmpnn/check_status/<task_id>", "description": "Checks LigandMPNN task processing status."},
]

@tasks_bp.route("/", methods=["GET"])
def list_tasks():
    """List all available tasks along with their descriptions and API endpoints."""
    return jsonify({
        "available_tasks": TASKS,
        "last_updated": datetime.datetime.utcnow().isoformat() + "Z"
    })
