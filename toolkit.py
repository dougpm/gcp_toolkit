from google.cloud import bigquery
import string

def bq_to_bucket(bq_client, storage_client, staging_dataset, bucket_url, sql):

    """Runs SQL in BigQuery and stores results in Storage"""

    letters = string.ascii_lowercase
    staging_table = '{}.temp_table'.format(staging_dataset) + ''.join(random.choice(letters) for i in range(120))
    
    job_config = bq_client.QueryJobConfig()
    job_config.destination = staging_table

    query_job = bq.query(sql, job_config=job_config)

    query_job.result()

    extract_job = bq.extract_table(staging_table, bucket_url)
    extract_job.result()

    bq.delete_table(staging_table)

