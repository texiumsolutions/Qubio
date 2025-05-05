import os
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()



# Azure AD credentials
tenant_id = os.getenv("AZURE_TENANT_ID")
client_id = os.getenv("AZURE_CLIENT_ID")  # Application (client) ID
client_secret = os.getenv("AZURE_CLIENT_SECRET")  # Client secret (keep this secure)

# Storage account details
account_name = "biotex"
storage_url = f"https://{account_name}.blob.core.windows.net"

# Authenticate using Azure AD
credential = ClientSecretCredential(tenant_id, client_id, client_secret)

# Connect to the Blob Storage account
blob_service_client = BlobServiceClient(account_url=storage_url, credential=credential)

# List containers
print("Listing containers:")
containers = blob_service_client.list_containers()
for container in containers:
    print(container["name"])
