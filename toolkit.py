import string
import random
from google.cloud import bigquery, storage

def bq_to_bucket(bq_client, storage_client, staging_dataset, bucket_url, sql):

    """Runs SQL in BigQuery and stores results in Storage"""

    letters = string.ascii_lowercase
    staging_table = '{}.{}.temp_table'.format(bq_client.project, staging_dataset) + ''.join(random.choice(letters) for i in range(120))
    
    job_config = bigquery.QueryJobConfig()
    job_config.destination = staging_table

    query_job = bq_client.query(sql, job_config=job_config)

    query_job.result()

    extract_job = bq_client.extract_table(staging_table, bucket_url)
    extract_job.result()

    bq_client.delete_table(staging_table)

#TODO: bucket_to_df
#TODO: bq_to_df


