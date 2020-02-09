from google.cloud import storage

def create_bucket_folder(bucket_name, folder_name, storage_client=storage.Client()):

    """Creates a Folder in Storage"""
    
    if '/' not in folder_name:
        folder_name = folder_name + '/'
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(folder_name)
    blob.upload_from_string('')