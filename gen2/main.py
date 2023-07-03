# Copyright 2023 Redis, Inc.

import os

from google.cloud import storage
import google.cloud.logging
import logging
import redis
import json
import functions_framework

client = google.cloud.logging.Client(project="central-beach-194106")
client.setup_logging()

redis_host = os.environ.get("REDISHOST", "localhost")
redis_port = int(os.environ.get("REDISPORT", 6379))
redis_password = os.environ.get("REDISPASSWORD", "")
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)

storage_client = storage.Client()

@functions_framework.cloud_event
def glau_gcs_redis_func_gen2(cloud_event):
    data: Dict = cloud_event.data
    event_id = cloud_event["id"]
    event_type = cloud_event["type"]
    bucket_name = data["bucket"]
    file_name = data["name"]
    logging.info(f"The file name is {file_name}");
    logging.info(f"The bucket name is {bucket_name}")

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)

    with blob.open("r") as f:
        key = "austin_crime:"
        for file_line in f:
            # convert to JSON
            json_obj = json.loads(file_line)
            redis_client.json().set(key+json_obj['unique_key'], '$', json_obj)

