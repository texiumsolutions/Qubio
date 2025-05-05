import os
import glob
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

# Azure Storage Configuration
connection_string = os.getenv("AZURE_CONNECTION_STRING")  # Ensure this is set in your environment
container_name = "proteinfold"


def generate_sas_url(blob_service_client, container_name, blob_path, expiry_hours=1):
    """
    Returns a pre-generated SAS URL using a static SAS token (from Azure Portal).
    """
    static_sas_token = os.getenv("AZURE_STATIC_SAS_TOKEN")  # Store this token in your .env

    if not static_sas_token:
        raise Exception("AZURE_STATIC_SAS_TOKEN not found in environment variables")

    # Optional debug info
    print(f"Generating SAS URL for: {blob_path}")


    return f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_path}?{static_sas_token}"


def get_task_type(task_output_folder):
    """
    Extracts the task type (e.g., 'antifold') from the path: outputs/antifold/taskid/
    """
    parts = task_output_folder.split(os.sep)
    try:
        index = parts.index("outputs")
        return parts[index + 1]
    except ValueError:
        raise ValueError(f"Invalid task_output_folder structure: {task_output_folder}")

def upload_task_outputs(task_id, task_output_folder):
    """
    Uploads all files in the task's output folder to Azure Blob Storage and returns SAS URLs.
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        task_type = get_task_type(task_output_folder)
        print(f"Detected Task Type: {task_type}")  # Optional: keep for debug

        files = glob.glob(os.path.join(task_output_folder, "*"))
        uploaded_files = []

        for file_path in files:
            filename = os.path.basename(file_path)
            blob_path = f"outputs/{task_type}/{task_id}/{filename}"
            blob_client = container_client.get_blob_client(blob_path)

            with open(file_path, "rb") as file:
                blob_client.upload_blob(file, overwrite=True)

            sas_url = generate_sas_url(blob_service_client, container_name, blob_path)
            uploaded_files.append(sas_url)

        return {"task_id": task_id, "uploaded_files": uploaded_files}

    except Exception as e:
        return {"error": str(e)}
