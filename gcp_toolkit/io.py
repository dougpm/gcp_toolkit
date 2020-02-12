import string
import random
import logging
from google.cloud import bigquery, storage
import pandas as pd
import gcp_toolkit.utils as gtku

#TODO: separate bq and storage classes

class IO:
    def __init__(self, bucket_name, bq_client=None, storage_client=None):
        self.bq_client = bigquery.Client() if bq_client is None else bq_client
        self.storage_client = storage.Client() if storage_client is None else storage_client
        try:
            self.bucket = self.storage_client.get_bucket(bucket_name)
        except Exception as e:
            if '403' in str(e):
                print("User doesn't have access to {}".format(bucket_name))
            if '404' in str(e):
                print("Bucket {} doesn't exist".format(bucket_name))
            else:
                print(e)
    def bq_to_bucket(self, query, path_to_file, staging_dataset=None):

        """Runs query in BigQuery and stores results in Storage"""

        if staging_dataset is None:
            raise
            #TODO: create random staging dataset function in utils, call it in constructor

        bucket_file_url = 'gs://{}/{}'.format(self.bucket_name, path_to_file)
        letters = string.ascii_lowercase
        staging_table = '{}.{}.temp_table'.format(self.bq_client.project, staging_dataset) + ''.join(random.choice(letters) for i in range(100))
        
        job_config = bigquery.QueryJobConfig()
        job_config.destination = staging_table
        query_job = self.bq_client.query(query, job_config=job_config)

        query_job.result()

        extract_job = self.bq_client.extract_table(staging_table, bucket_file_url)
        extract_job.result()

        #TODO: finally statement or context manager
        self.bq_client.delete_table(staging_table)

    def bucket_to_df(self, path_to_file):

        """Reads a file or a group of files matching a pattern into a pandas Data Frame"""

        df = pd.DataFrame()
        partial_df = pd.DataFrame()
        bucket = self.storage_client.get_bucket(self.bucket_name)
        blobs = bucket.list_blobs()
        for blob in blobs:
            if path_to_file in blob.name:
                url = 'gs://{}/{}'.format(self.bucket_name, blob.name)
                #TODO: more file formats
                partial_df = pd.read_csv(url, index_col=False, low_memory=False)
                df = df.append(partial_df)
        
        return df


    def bq_to_df(self, query, staging_dataset=None, use_builtin=False):
        
        """Runs a query in BigQuery and loads the results into a pandas Data Frame"""
        
        if use_builtin:
            query_job = self.bq_client.query(query)  
            return query_job.result().to_dataframe()

        if staging_dataset is None:
            raise
            #TODO: create random staging dataset function in utils, call it in constructor

        #it takes way too long to load very large tables with to_dataframe(), so doing the following is faster:

        letters = string.ascii_lowercase
        staging_blob = ''.join(random.choice(letters) for i in range(100)) + '/'
        gtku.create_bucket_folder(self.bucket_name, staging_blob)
        print('Created {}'.format(staging_blob))
        
        self.bq_to_bucket(query, 'gs://{}/{}results*'.format(self.bucket_name, staging_blob), staging_dataset)
        df = self.bucket_to_df('{}results'.format(staging_blob))

        #TODO: finally statement or context manager
        bucket = self.storage_client.get_bucket(self.bucket_name)
        bucket.delete_blob(staging_blob)

        return df


    def df_to_bq(self, df, table_id, schema=[]):

        """Writes a pandas Data Frame to a BigQuery table."""

        job_config = bigquery.LoadJobConfig(schema=schema)
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
        job = self.bq_client.load_table_from_dataframe(df, table_id, job_config=job_config)
        
        job.result()


