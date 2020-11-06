import statsmodels.api as sm
import boto3
import json
import os

bucket = os.environ['bucket']
key_template = os.environ['keyTemplate']
s3  = boto3.resource('s3')

def get_model(model_id):
    key = key_template.format(id=model_id)
    tmp = '/tmp/{id}.pickle'.format(id=model_id)
    s3.Bucket(bucket).download_file(key, tmp)
    model = sm.load(tmp)
    return model

def predict_from_model(model, data):
    prediction = model.predict(exog=data)
    return prediction[0]

def lambda_handler(event, context):
    payload = json.loads(event['body'])
    model   = get_model(payload['modelId'])
    prediction = predict_from_model(model=model, data=payload['data'])

    result = {
        'prediction': prediction
    }

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
