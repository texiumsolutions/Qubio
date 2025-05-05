from azure.storage.blob import BlobServiceClient
import os

# Azure Storage Configuration
STORAGE_ACCOUNT_NAME = "your_storage_account"
STORAGE_ACCOUNT_KEY = "your_storage_account_key"
CONTAINER_NAME = "your_container_name"

connection_string = f"DefaultEndpointsProtocol=https;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

def upload_to_blob(local_file_path, blob_name):
    """ Uploads a file to Azure Blob Storage """
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)

    with open(local_file_path, "rb") as file:
        blob_client.upload_blob(file, overwrite=True)

    return blob_client.url  # Return the URL of the uploaded file
