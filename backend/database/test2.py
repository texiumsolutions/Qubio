import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure Storage account credentials from .env
AZURE_STORAGE_ACCOUNT_NAME = "biotex"  # Change this to your storage account name
AZURE_BLOB_CONTAINER = "proteinfold"  # Change this to your container name
BLOB_NAME = "yourfile.txt"  # Change this to the blob (file) you want to download
DOWNLOAD_PATH = "downloaded_file.txt"  # Where to save the file locally

# Load credentials from environment variables
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")

# Create a BlobServiceClient using DefaultAzureCredential
from azure.identity import ClientSecretCredential

credential = ClientSecretCredential(AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)
blob_service_client = BlobServiceClient(
    account_url=f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
    credential=credential
)

# Get the container client
container_client = blob_service_client.get_container_client(AZURE_BLOB_CONTAINER)

# Download the blob
blob_client = container_client.get_blob_client(BLOB_NAME)
with open(DOWNLOAD_PATH, "wb") as download_file:
    download_file.write(blob_client.download_blob().readall())

print(f"✅ File '{BLOB_NAME}' downloaded successfully as '{DOWNLOAD_PATH}'")
