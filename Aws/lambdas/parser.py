import boto3
import os
import sys
import uuid
import json
from urllib.parse import unquote_plus
import pandas as pd # solution -> https://korniichuk.medium.com/lambda-with-pandas-fd81aa2ff25e
import flatten_json
import requests

s3_client = boto3.client('s3')


def lambda_handler(event, context):
  for record in event['Records']:
      bucket = record['s3']['bucket']['name']
      fileName = unquote_plus(record['s3']['object']['key'])
      tempFileName = fileName.replace('input/', '')
      #ein unique dateiname wird erstellt in dem ordener temp (in der lambda)
      file_local_path = '/tmp/{}'.format(tempFileName)
      s3_client.download_file(bucket, fileName, file_local_path)
      tempFileNameWithoutSuffix = tempFileName.replace('.json', '')
      convert_to_flat_csv(file_local_path, tempFileNameWithoutSuffix)
      s3_client.upload_file("/tmp/{}.csv".format(tempFileNameWithoutSuffix), "haidi-ki-s3", "output/{}.csv".format(tempFileNameWithoutSuffix))
      notify_backend(bucket, "output/{}.csv".format(tempFileNameWithoutSuffix))


      
def convert_to_flat_csv(file_path, key):
  with open(file_path) as file:
    # Flattens the json file while renaming nested items like "mediaBox" : {"x" : 0.0, "y" : 0.0} into flat keys like mediaBox_x: 0.0 and mediaBox_y: 0.0
    s = flat_json(file)
    df = pd.json_normalize(s)
                        
  df.to_csv("/tmp/{}.csv".format(key), index=False)


# Flattens .json at given path to not contain any nested structures
def flat_json(file):
    s = json.load(file)
    flattened_json = flatten_json.flatten(s)
    return flattened_json
 

 
def json_filter(unfiltered_dict):
    data_dict = {}
    data_dict['documentId'] = unfiltered_dict['documentId']
    data_dict['name'] = unfiltered_dict['name']
    data_dict['mediaBox_width'] = unfiltered_dict['mediaBox_width']
    data_dict['mediaBox_height'] = unfiltered_dict['mediaBox_height']
 
    for label in unfiltered_dict:
        if "trimBox" in label:
            data_dict[label] = unfiltered_dict[label]
        if "color" in label:
            data_dict[label] = unfiltered_dict[label]
    return data_dict

def notify_backend(bucket, filename):
    filename_parts = filename.split('-')
    ip = filename_parts[1].replace('.csv', '')
    
    url = "http://{}/api/parsed".format(ip)
    myjson = {
        "status": "PARSED",
        "bucketname": bucket,
        "fileUri": filename
    }
    
    try:
        x = requests.post(url, json = myjson, timeout=1)
        print(x.text)
    except:
        print("Timeout from node-backend with ip {}".format(ip))
