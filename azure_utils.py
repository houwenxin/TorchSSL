import os

account_name = ""
account_key = ""
connect_str = ""
container_name = ""

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield root, f

def save_to_azure(local_file_path, azure_file_path, service='blob'):
    '''Save files to Azure.
    Install: pip install azure-storage-blob
    Params:
        local_file_path: full path to the local file.
        azure_file_path: file full path on Azure. Can be 'abcd/efgh/a.log'.
        service: 'fileshare' or 'blob'. NOTE: if service='fileshare', your azure_file_path must not contain directories!
    '''
    if service == 'fileshare':
        from azure.storage.file import FileService
        file_service = FileService(account_name=account_name, account_key=account_key)
        file_service.create_file_from_path('logs', None, azure_file_path, local_file_path)
    elif service == 'blob':
        from azure.storage.blob import BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        
        blob_client = blob_service_client.get_blob_client(container=container_name, blob='train/flexmatch/' + azure_file_path)
        if os.path.isdir(local_file_path):
            for root, f in findAllFile(local_file_path):
                path = os.path.join(root, f)
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.join('train/flexmatch/', azure_file_path, f))
                try:
                    with open(path, "rb") as data:
                        blob_client.upload_blob(data)
                except:
                    blob_client.delete_blob()
                    with open(path, "rb") as data:
                        blob_client.upload_blob(data)
        else:
            try:
                with open(local_file_path, "rb") as data:
                    blob_client.upload_blob(data)
            except:
                blob_client.delete_blob()
                with open(local_file_path, "rb") as data:
                    blob_client.upload_blob(data)
    else:
        raise ValueError('Service not correct! Must be fileshare or blob!')