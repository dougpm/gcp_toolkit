from google.cloud import storage, bigquery

def create_bucket_folder(bucket_name, folder_name, storage_client=None):

    """Creates a Folder in Storage"""

    if storage_client is None:
        storage_client = storage.Client()
    if '/' not in folder_name:
        folder_name = folder_name + '/'
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(folder_name)
    blob.upload_from_string('')

def convert_pandas_gbq_schema(schema):
    
    """Converts a BigQuery schema in the format of a list of dicts, used by pandas gbq
    into a list of SchemaFields"""
    
    new_schema = []
    for field in schema:
        new_schema.append(bigquery.SchemaField(field['name'], field['type']))
    return new_schema

#TODO: create dataset
#TODO: create bq table
#TODO: create bq table schema