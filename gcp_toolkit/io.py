import string
import random
import logging
from google.cloud import bigquery, storage
import pandas as pd
import gcp_toolkit.utils as gtku

#TODO: separate bq and storage classes
#TODO: tests
class IO:
    def __init__(self, bucket_name, staging_dataset, bq_client=None, storage_client=None):
        self.bq_client = bigquery.Client() if bq_client is None else bq_client
        self.storage_client = storage.Client() if storage_client is None else storage_client
        self.bucket_name = bucket_name
        self.staging_dataset = staging_dataset
        try:
            self.bucket = self.storage_client.get_bucket(bucket_name)
        except Exception as e:
            if '403' in str(e):
                print("User doesn't have access to {}".format(bucket_name))
            elif '404' in str(e):
                print("Bucket {} doesn't exist".format(bucket_name))
            else:
                print(e)
        try:
            self.bq_client.get_dataset(staging_dataset)
        except Exception as e:
            if '403' in str(e):
                print("User doesn't have access to {}".format(staging_dataset))
            elif '404' in str(e):
                print("Dataset {} doesn't exist".format(staging_dataset))

    def bq_to_bucket(self, query, path_to_file):

        """Runs query in BigQuery and stores results in Storage"""

        bucket_file_url = 'gs://{}/{}'.format(self.bucket_name, path_to_file)
        letters = string.ascii_lowercase
        staging_table = '{}.{}.temp_table_'.format(self.bq_client.project, self.staging_dataset) + ''.join(random.choice(letters) for i in range(100))
        
        job_config = bigquery.QueryJobConfig()
        job_config.destination = staging_table
        query_job = self.bq_client.query(query, job_config=job_config)
        query_job.result()
        extract_job = self.bq_client.extract_table(staging_table, bucket_file_url)
        extract_job.result()
        self.bq_client.delete_table(staging_table)

    def bucket_to_df(self, path_to_file):

        """Reads a file or a group of files matching a pattern into a pandas Data Frame"""

        df = pd.DataFrame()
        partial_df = pd.DataFrame()
        blobs = self.bucket.list_blobs()
        for blob in blobs:
            if path_to_file in blob.name:
                url = 'gs://{}/{}'.format(self.bucket_name, blob.name)
                #TODO: more file formats
                partial_df = pd.read_csv(url, index_col=False, low_memory=False)
                df = df.append(partial_df)
        
        return df

    def bq_to_df(self, query, use_builtin=False):
        
        """Runs a query in BigQuery and loads the results into a pandas Data Frame"""
        
        if use_builtin:
            query_job = self.bq_client.query(query)  
            return query_job.result().to_dataframe()

        #it takes way too long to load very large tables with to_dataframe(), so doing the following is faster:
        letters = string.ascii_lowercase
        staging_blob = ''.join(random.choice(letters) for i in range(100)) + '/'
        gtku.create_bucket_folder(self.bucket_name, staging_blob)
        try:
            self.bq_to_bucket(query, 'gs://{}/{}results*'.format(self.bucket_name, staging_blob))
            df = self.bucket_to_df('{}results'.format(staging_blob))
        finally:
            bucket = self.storage_client.get_bucket(self.bucket_name)
            bucket.delete_blob(staging_blob)

        return df


    def df_to_bq(self, df, table_id, schema=[]):

        """Loads a pandas Data Frame into a BigQuery table."""

        job_config = bigquery.LoadJobConfig()
        if schema:
            job_config.schema = schema
        else:
            job_config.autodetect = True
        #TODO: options
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
        job = self.bq_client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()

    def bucket_to_bq(self, path_to_file, table_id, schema=[], csv_delimiter=','):

        """Loads a csv from Storage into a BigQuery table"""

        job_config = bigquery.LoadJobConfig()
        if schema:
            job_config.schema = schema
        else:
            job_config.autodetect = True
        #TODO: options
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
        job_config.field_delimiter = csv_delimiter
        source = 'gs://{}/{}'.format(self.bucket_name, path_to_file)
        job = self.bq_client.load_table_from_uri(source, table_id, job_config=job_config)
        job.result()
    