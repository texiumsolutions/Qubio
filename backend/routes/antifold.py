import os
import logging
import uuid
import urllib.parse
import requests
from flask import Blueprint, request, jsonify
from backend.services.antifold_service import run_antifold
from backend.database.azure_upload import upload_task_outputs

antifold_bp = Blueprint("antifold", __name__)



UPLOAD_FOLDER = "/home/texsols/BioTasks/uploads"
OUTPUT_FOLDER = "/home/texsols/BioTasks/outputs/antifold_output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        logging.info(f"Downloaded file from URL to {save_path}")
        return save_path
    except requests.exceptions.RequestException as e:
        logging.error(f"Download failed from URL: {url} - {e}")
        raise Exception(f"Download failed from URL: {url} - {e}")

@antifold_bp.route("/predict", methods=["POST"])
def predict():
    try:
        task_type = request.form.get("task_type")
        heavy_chain = request.form.get("heavy_chain")
        light_chain = request.form.get("light_chain")
        task_id = str(uuid.uuid4())

        pdb_file = request.files.get("pdb_file")
        pdb_url = request.form.get("pdb_file_url")

        if not pdb_file and not pdb_url:
            logging.error("No PDB file provided (upload or URL).")
            return jsonify({"error": "No PDB file provided (upload or URL)."}), 400

        if pdb_file:
            pdb_filename = f"{task_id}_{pdb_file.filename}"
            pdb_filepath = os.path.join(UPLOAD_FOLDER, pdb_filename)
            pdb_file.save(pdb_filepath)
            logging.info(f"PDB file uploaded and saved to {pdb_filepath}")
        else:
            parsed_url = urllib.parse.urlparse(pdb_url)
            filename = os.path.basename(parsed_url.path)
            filename = filename if filename.endswith(".pdb") else f"{filename}.pdb"
            pdb_filename = f"{task_id}_{filename}"
            pdb_filepath = os.path.join(UPLOAD_FOLDER, pdb_filename)
            logging.info(f"Downloading PDB file from signed URL: {pdb_url}")
            download_file(pdb_url, pdb_filepath)

        params = {
            "task_type": task_type,
            "pdb_file": pdb_filepath,
            "heavy_chain": heavy_chain,
            "light_chain": light_chain,
            "task_id": task_id
        }

        logging.info(f"Running AntiFold with task ID: {task_id}")
        result = run_antifold(params)
        return jsonify(result)

    except Exception as e:
        logging.error(f"Error in predict: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@antifold_bp.route("/check_status/<task_id>", methods=["GET"])
def check_status(task_id):
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
