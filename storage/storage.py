import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
load_dotenv()

# Blob storage configuration
storage_account_key = os.environ.get("STORAGE_ACCOUNT_KEY")
storage_account_name = os.environ.get("STORAGE_ACCOUNT_NAME")
storage_container_string = os.environ.get("BLOB_STORAGE_CONNECTION_STRING")
blob_container_name = os.environ.get("BLOB_CONTAINER_NAME")

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(storage_container_string)

def get_blob_client(filename: str):
    return blob_service_client.get_blob_client(container=blob_container_name, blob=filename)

def upload_to_blob(file, filename: str):
    blob_client = blob_service_client.get_blob_client(container=blob_container_name, blob=filename)
    blob_client.upload_blob(file)