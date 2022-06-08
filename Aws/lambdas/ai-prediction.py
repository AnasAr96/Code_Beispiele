
#Achtung die lambda muss muss als ÜbergabeParameter mindestens 2 Objekte bekommen
#{
#  "filename": "testOrdner/testData.csv",
#  "bucketName": "haidi-ki-s3"
#}


import os
import io
import boto3
import json
import pandas as pd
import csv
from io import StringIO
from botocore.config import Config


# grab environment variables
ENDPOINT_NAME = "multiModel-V1-2022-02-01-11-35-02"  # typ Endpoint
client = boto3.client('s3')
config = Config(
    read_timeout=70,
    retries={
        'max_attempts': 2  # This value can be adjusted to 5 to go up to the 360s max timeout
    }
)
runtime = boto3.client('sagemaker-runtime', config=config)


def changeName (param):
    if param =="DIN_A0_Hoch":
        return "DIN A0 Hochformat "
    elif param == "DIN_A0_Quer":
        return "DIN A0 Querformat"
    elif param == "DIN_A1_Hoch":
        return "DIN A1 Hochformat"
    elif param == "DIN_A1_Quer":
        return "DIN A1 Querformat"
    elif param == "Freies_Format":
        return "freies Format"
    elif param == "DIN_A4_Hoch":
        return "DIN A4 Hochformat"
    elif param == "DIN_A4_Quer":
        return "DIN A4 Querformat"
    elif param == "DIN_A5_Hoch":
        return "DIN A5 Hochformat"
    elif param == "DIN_A5_Quer":
        return "DIN A5 Querformat"
    elif param == "DIN_A6_Hoch":
        return "DIN A6 Hochformat"
    elif param == "DIN_A6_Quer":
        return "DIN A6 Querformat"
    elif param == "gestrichen_altes_Profil":
        return "Gestrichen (altes Profil)"
    elif param == "gestrichen_neues_Profil":
        return "Gestrichen (neues Profil)"
    elif param == "angestrichen_altes_Profil":
        return "Angestrichen (altes Profil)"
    elif param == "angestrichen_neues_Profil":
        return "Angestrichen (neues Profil)"
    elif param == "etikett" :
        return "Etikett"
    elif param == "poster" :
        return "Poster"
    elif param == "flyer" :
        return "Flyer"
    else:
        return param


def makeDummy(output_intent):
    dummy_list = [{'output_intent_F39': 0, 'output_intent_F47': 0, 'output_intent_F51': 0, 'output_intent_F52': 0,
                   'output_intent_F78': 0
                      , 'output_intent_undefinde': 0}]
    dummy_df = pd.DataFrame(dummy_list)

    if output_intent == 'F39':
        dummy_df['output_intent_F39'] = 1

    elif output_intent == 'F47':
        dummy_df['output_intent_F47'] = 1

    elif output_intent == 'F51':
        dummy_df['output_intent_F51'] = 1

    elif output_intent == 'F52':
        dummy_df['output_intent_F51'] = 1

    elif output_intent == 'F78':
        dummy_df['output_intent_F78'] = 1

    elif output_intent == 'undefinde':
        dummy_df['output_intent_undefinde'] = 1

    return dummy_df


def get_predictions_dict (payload):
    predictions_dict = {
        "size": "",
        "papertype": "",
        "producttype": "",
        "duplex": ""
    }
    values = ["duplex", "size", "papertype", "producttype"]
    i = 0

    for model in ['druckseiten.tar.gz', 'format.tar.gz', 'papriertyp.tar.gz', 'typ.tar.gz']:
        response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME, TargetModel=model,
                                           ContentType='text/csv', Body=payload)
        result = json.loads(response['Body'].read().decode())
        predictions_dict[values[i]] = changeName (result[0])
        i = i + 1

    return predictions_dict


def lambda_handler(event, context):
    param = json.loads(json.dumps(event))
    print("####EVENT####" , param , "####EVENT END####")

    key = param['filename']
    bucket = param['bucketName']
    s3_resource = boto3.resource('s3')

    csv_obj = client.get_object(Bucket=bucket, Key=key)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    dataset = pd.read_csv(StringIO(csv_string))

    if set(['mediaBox_width']).issubset(dataset) == False:
        print("invalid csv file")

        return

    data = pd.DataFrame(dataset, columns=['mediaBox_width', 'mediaBox_height', 'seiten_anzahl'], index=None)
    output_intent = pd.DataFrame(dataset, columns=['output_intent'], index=None)

    one_hot_key_output_intent = makeDummy(output_intent=output_intent.values)

    data = pd.concat([data, one_hot_key_output_intent], axis=1)
    payload = data.to_csv(header=False, index=False)

    predictions_dict = get_predictions_dict(payload)

    print("######data : " ,data.to_string())
    print("######predictions_dict" , predictions_dict.items())

    print("######function terminated")

    return predictions_dict
