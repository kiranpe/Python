#!/usr/bin/env python3

import os
import sys
import datetime as dt
from google.cloud import storage

def copy_cloud_function():
    todayDate = os.popen("date +'%Y-%m-%d'").read().strip()
    print(todayDate)
    bucket_name = "seg-cmp-ods-us"
    storage_client = storage.Client()
    source_bucket = storage_client.bucket(bucket_name)
    destination_bucket_name = "seg-cmp-ods-us"
    destination_bucket = storage_client.bucket(destination_bucket_name)
    list_of_blobs = source_bucket.list_blobs(prefix='ods/requests/')
    list_of_files = []
    for x in list_of_blobs:
      if str(x.name).endswith('.json'):
         list_of_files.append({'name': x.name, 'time': x.time_created})
    for idx in range(len(list_of_files)):
      fTime = os.popen("echo {} | cut -d ' ' -f1".format(list_of_files[idx]['time'])).read().strip()
      if fTime == todayDate:
       latestblob = list_of_files[idx]['name']

       blob = os.popen("echo {} | cut -d '/' -f3".format(latestblob)).read().strip()
       blob_name = f"ods/requests/{blob}"
       source_blob = source_bucket.blob(blob_name)
       destination_blob_name = f"ods/requests/test/{blob}"
       blob_copy = source_bucket.copy_blob(
         source_blob, destination_bucket, destination_blob_name
       )

       print(f"Blob {source_blob.name} in bucket {source_bucket.name} copied to blob {blob_copy.name} in bucket {destination_bucket.name}.")

    return "Copied files Successfully!!"
    
copy_cloud_function()
