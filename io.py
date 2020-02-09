import string
import random
import logging
from google.cloud import bigquery, storage
import pandas as pd
import gcp_toolkit.utils as gtku

def bq_to_bucket(query, bucket_file_url, staging_dataset=None, bigquery_client=None, storage_client=None):

    """Runs query in BigQuery and stores results in Storage"""

    if bigquery_client is None:
        bigquery_client = bigquery.Client()
    if storage_client is None:
        storage_client = storage.Client()
    if staging_dataset is None:
        return
        #TODO: create random staging dataset
    letters = string.ascii_lowercase
    staging_table = '{}.{}.temp_table'.format(bigquery_client.project, staging_dataset) + ''.join(random.choice(letters) for i in range(100))
    
    job_config = bigquery.QueryJobConfig()
    job_config.destination = staging_table

    query_job = bigquery_client.query(query, job_config=job_config)

    query_job.result()

    extract_job = bigquery_client.extract_table(staging_table, bucket_file_url)
    extract_job.result()

    bigquery_client.delete_table(staging_table)

def bucket_to_df(bucket_name, path_to_file, storage_client=None):

    """Reads a file or a group of files matching a pattern into a pandas Data Frame"""

    if storage_client is None:
        storage_client = storage.Client()

    df = pd.DataFrame()
    partial_df = pd.DataFrame()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()
    for blob in blobs:
        if path_to_file in blob.name:
            url = 'gs://{}/{}'.format(bucket_name, blob.name)
            #TODO: more file formats
            partial_df = pd.read_csv(url, index_col=False, low_memory=False)
            df = df.append(partial_df)
    
    return df


def bq_to_df(query, bucket_name, staging_dataset=None, bigquery_client=None, storage_client=None):
    
    """Runs a query in BigQuery and loads the results into a pandas Data Frame"""
    if bigquery_client is None:
        bigquery_client = bigquery.Client()
    if storage_client is None:
        storage_client = storage.Client()

    letters = string.ascii_lowercase
    staging_blob = ''.join(random.choice(letters) for i in range(100)) + '/'
    gtku.create_bucket_folder(bucket_name, staging_blob)
    print('Created {}'.format(staging_blob))
    
    bq_to_bucket(query, 'gs://{}/{}results'.format(bucket_name, staging_blob), staging_dataset, bigquery_client, storage_client)
    df = bucket_to_df(bucket_name, '{}/{}results'.format(bucket_name, staging_blob), storage_client)

    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete_blob(staging_blob)

    return df
    #TODO: create temporary bucket folder
    #create temporary dataset
    #call bq_to_bucket using temporary bucket and dataset
    #call bucket_to_df using temp bucket and file names

#TODO: df_to_bq


