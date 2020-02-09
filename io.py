import string
import random
import logging
from google.cloud import bigquery, storage
import pandas as pd
import gcp_toolkit.utils as gtku

#TODO: separate bq and storage classes
class IO:
    def __init__(self, bucket_name, bq_client=None, storage_client=None):
        self.bucket_name = bucket_name
        self.bq_client = bigquery.Client() if bq_client is None else bq_client
        self.storage_client = storage.Client() if storage_client is None else storage_client

    def bq_to_bucket(self, query, path_to_file, staging_dataset=None):

        """Runs query in BigQuery and stores results in Storage"""

        if staging_dataset is None:
            return
            print('no staging_dataset in bq_to_bucket')
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


    def bq_to_df(self, query, staging_dataset=None):
        
        """Runs a query in BigQuery and loads the results into a pandas Data Frame"""

        if staging_dataset is None:
            return
            print('no staging_dataset in bq_to_bucket')
            #TODO: create random staging dataset function in utils, call it in constructor

        letters = string.ascii_lowercase
        staging_blob = ''.join(random.choice(letters) for i in range(100)) + '/'
        gtku.create_bucket_folder(self.bucket_name, staging_blob)
        print('Created {}'.format(staging_blob))
        
        bq_to_bucket(query, 'gs://{}/{}results'.format(self.bucket_name, staging_blob), staging_dataset, self.bq_client, self.storage_client)
        df = bucket_to_df(self.bucket_name, '{}results'.format(staging_blob), self.storage_client)

        #TODO: finally statement or context manager
        bucket = self.storage_client.get_bucket(self.bucket_name)
        bucket.delete_blob(staging_blob)

        return df

#TODO: df_to_bq


