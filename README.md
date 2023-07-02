# gcp_cloud_function_bigquery_gcs_redis

Deploy Cloud Function:
```bash
cd python
gcloud functions deploy glau_gcs_redis_func \
--runtime=python311 \
--region=us-central1 \
--source=. \
--trigger-bucket=glau-test-bucket-us-central1 \
--allow-unauthenticated \
--set-env-vars=REDISHOST=redis-10996.c279.us-central1-1.gce.cloud.redislabs.com,REDISPORT=10996,REDISPASSWORD=xnurcS28JREs9S8HHemx2cKc1jLFi3ua
```
    
Export BigQuery table to the GCS bucket "glau-test-bucket-us-central1" in JSON format.
```bash
cd BQ_2_GCS
python3 extract.py
```    


