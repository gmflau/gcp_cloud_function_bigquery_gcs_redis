# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_memorystore_redis]

import os

from google.cloud import storage
import functions_framework
import google.cloud.logging
import logging
import redis
import json
from redis.commands.json.path import Path

client = google.cloud.logging.Client(project="project")
client.setup_logging()

redis_host = os.environ.get("REDISHOST", "localhost")
redis_port = int(os.environ.get("REDISPORT", 6379))
redis_password = os.environ.get("REDISPASSWORD", "")
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)

storage_client = storage.Client()

#@functions_framework.http
def glau_gcs_redis_func(data, context):
    file_data = data
    file_name = file_data["name"]
    print(f"The image is {file_name}")
    logging.info(f"The image is {file_name}");
    bucket_name = file_data["bucket"]
    print(f"The bucket_name is {bucket_name}")
    logging.info(f"The bucket_name is {bucket_name}")
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    #f = blob.download_as_text(encoding="utf-8")
    #logging.info(f"The downloaded text is {f}")

    with blob.open("r") as f:
        key = "austin_crime:"
        counter = 0
        for file_line in f:
            print(file_line)
            logging.info(file_line)
            # convert to JSON
            json_obj = json.loads(file_line)
            # use realine() to read next line
            redis_client.set(key+str(counter), file_line)
            redis_client.json().set(key+json_obj['unique_key'], '$', json_obj)
            counter=counter+1
            value = redis_client.incr("visits", 1)
            #return f"Visit count: {value}"


# [END functions_memorystore_redis]
