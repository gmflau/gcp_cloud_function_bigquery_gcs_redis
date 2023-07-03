# gcp_cloud_function_bigquery_gcs_redis

Deploy Cloud Function:
Gen1:
```bash
gcloud functions deploy glau_gcs_redis_func \
--runtime=python311 \
--region=us-central1 \
--source=./gen1 \
--trigger-bucket=glau-test-bucket-us-central1 \
--allow-unauthenticated \
--set-env-vars=REDISHOST=redis-10996.c279.us-central1-1.gce.cloud.redislabs.com,REDISPORT=10996,REDISPASSWORD=xnurcS28JREs9S8HHemx2cKc1jLFi3ua
```
   
Gen2: 
```bash
export PROJECT_ID=$(gcloud info --format='value(config.project)')

SERVICE_ACCOUNT="$(gsutil kms serviceaccount -p ${PROJECT_ID})"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
--member="serviceAccount:${SERVICE_ACCOUNT}" \
--role='roles/pubsub.publisher' \
--condition='None'

gcloud functions deploy glau_gcs_redis_func_gen2 \
--gen2 \
--runtime=python311 \
--region=us-central1 \
--memory=4G \
--source=./gen2 \
--trigger-bucket=glau-test-bucket-us-central1 \
--allow-unauthenticated \
--entry-point=glau_gcs_redis_func_gen2 \
--set-env-vars=REDISHOST=redis-10996.c279.us-central1-1.gce.cloud.redislabs.com,REDISPORT=10996,REDISPASSWORD=xnurcS28JREs9S8HHemx2cKc1jLFi3ua
```

    
Export BigQuery table to the GCS bucket "glau-test-bucket-us-central1" in JSON format.
```bash
cd BQ_2_GCS
python3 extract.py
```    


