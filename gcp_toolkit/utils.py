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

def change_table_schema(table_id, new_fields, bigquery_client=None):

    """Updates a table schema with new fields"""
    
    bq_client = bigquery.Client() if bigquery_client is None else bigquery_client
    table = bq_client.get_table(table_id)
    original_schema = table.schema
    new_schema = original_schema[:]
    for name, field_type in new_fields:
        new_schema.append(bigquery.SchemaField("{}".format(name), "{}".format(field_type)))
    table.schema = new_schema
    table = client.update_table(table, ["schema"])



#TODO: create dataset
#TODO: create bq table
#TODO: create bq table schema