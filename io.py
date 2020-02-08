import string
import random
import logging
from google.cloud import bigquery, storage
import pandas as pd

def bq_to_bucket(sql, bucket_url, staging_dataset=None, bq_client=bigquery.Client(), storage_client=storage.Client()):

    """Runs SQL in BigQuery and stores results in Storage"""

    if staging_dataset is None:
        return
        #TODO: create random staging dataset
        
    letters = string.ascii_lowercase
    staging_table = '{}.{}.temp_table'.format(bq_client.project, staging_dataset) + ''.join(random.choice(letters) for i in range(100))
    
    job_config = bigquery.QueryJobConfig()
    job_config.destination = staging_table

    query_job = bq_client.query(sql, job_config=job_config)

    query_job.result()

    extract_job = bq_client.extract_table(staging_table, bucket_url)
    extract_job.result()

    bq_client.delete_table(staging_table)



def bucket_to_df(bucket_name, path_to_file, storage_client=storage.Client()):

    """Reads a file or a group of files matching a pattern into a pandas Data Frame"""

    df = pd.DataFrame()
    partial_df = pd.DataFrame()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()
    for blob in blobs:
        print(blob.name)
        if path_to_file in blob.name:
            url = 'gs://{}/{}'.format(bucket_name, blob.name)
            #TODO: more file formats
            partial_df = pd.read_csv(url, index_col=False, low_memory=False)
        df = df.append(partial_df)
    
    return df

    




#TODO: bq_to_df