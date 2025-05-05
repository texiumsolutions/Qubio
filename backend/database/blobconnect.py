from azure.storage.blob import BlobServiceClient, BlobClient ContainerClient
import os

connection_string = os.getenv("AZURE_CONNECTION_STRING")
container_name = "proteinfold"
blob_name = "jobname/test.txt"
file_path = "~/BioTasks/uploads"

def upload_to_blobl():
	try:
		blob_service_client=BlobServiceClient.from_connection_string(connection_string)
		container_client = blob_service_client.get_container_client(container_name)
		blob_client = container_client.get_blob_client(blob_name)
		
		with open(file_path, "r") as file:
			content = file.read()
		blob_client.upload_blob(content, overwrite=True)
		print(f"File {file_path} uploaded to Blobl Storage successfully")
	except Exception as e:
		print(f"Error occured: {e}")

if __name__== "__main__":
	upload_to_blob()
