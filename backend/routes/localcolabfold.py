import os
import logging
import uuid
import urllib.parse
import requests
from flask import Blueprint, request, jsonify
from backend.services.localcolabfold_service import run_localcolabfold
from backend.database.azure_upload import upload_task_outputs

localcolabfold_bp = Blueprint("localcolabfold", __name__)

UPLOAD_FOLDER = "/home/texsols/BioTasks/uploads"
OUTPUT_FOLDER = "/home/texsols/BioTasks/outputs/localcolabfold_output"
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

@localcolabfold_bp.route("/predict", methods=["POST"])
def predict():
    try:
        task_id = str(uuid.uuid4())
        fasta_file = request.files.get("fasta_file")
        fasta_url = request.form.get("fasta_file_url")

        if not fasta_file and not fasta_url:
            return jsonify({"error": "No FASTA file provided (upload or URL)."}), 400

        if fasta_file:
            fasta_filename = f"{task_id}_{fasta_file.filename}"
            fasta_path = os.path.join(UPLOAD_FOLDER, fasta_filename)
            fasta_file.save(fasta_path)
        else:
            parsed_url = urllib.parse.urlparse(fasta_url)
            filename = os.path.basename(parsed_url.path)
            filename = filename if filename.endswith(".fasta") else f"{filename}.fasta"
            fasta_filename = f"{task_id}_{filename}"
            fasta_path = os.path.join(UPLOAD_FOLDER, fasta_filename)
            download_file(fasta_url, fasta_path)

        result = run_localcolabfold(fasta_path, task_id)
        return jsonify(result)

    except Exception as e:
        logging.error(f"Error in LocalColabFold prediction: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@localcolabfold_bp.route("/check_status/<task_id>", methods=["GET"])
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
        logging.error(f"Error in LocalColabFold check_status: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
