from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobServiceClient
from config import config

azure_config = config(section='azure')
azure_account_key = azure_config['account_key']

def upload_blob():
    # Replace this with your actual connection string from Azure Portal
    connection_string = f"DefaultEndpointsProtocol=https;AccountName=storagetimereport;AccountKey={azure_account_key};EndpointSuffix=core.windows.net"
    # Name of the container where you want to upload the file
    container_name = "reports"
    # Local path to the file to upload


    # Name of the blob (filename in Azure)
    local_file_path = r"C:\Users\User\Documents\GitHub\Group_Project_group1\Project-root\time_management_api\report.txt"

    blob_name = "report.txt"
    
    # Create a BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get the container client
    container_client = blob_service_client.get_container_client(container_name)

    # Upload the file
    with open(local_file_path, "rb") as data:
        container_client.upload_blob(name=blob_name, data=data)
    print(f"Uploaded {blob_name} to container {container_name}")

if __name__ == "__main__":
    upload_blob()