from datetime import datetime
from google.cloud import bigquery
client = bigquery.Client()
bucket_name = 'glau-test-bucket-us-central1'

now = datetime.now()
project="bigquery-public-data"
dataset_id="austin_311"
dataset_id="austin_311"
table_name="311_service_requests"
destination_uri = "gs://{}/{}".format(bucket_name, "austin_crimes_" + now.strftime("%Y%m%d%H%M") + ".json")
dataset_ref = bigquery.DatasetReference(project, dataset_id)
table_ref = dataset_ref.table(table_name)
job_config = bigquery.job.ExtractJobConfig()
job_config.destination_format = bigquery.DestinationFormat.NEWLINE_DELIMITED_JSON

extract_job = client.extract_table(
    table_ref,
    destination_uri,
    job_config=job_config,
    # Location must match that of the source table.
    location="US",
)  # API request
extract_job.result()  # Waits for job to complete.
