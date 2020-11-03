import statsmodels.api as sm
import boto3
import tempfile
import json
import os

bucket = os.environ['statsmodelsBucket']
key_template = os.environ['statsmodelsKeyTemplate']
s3  = boto3.resource('s3')

def lambda_handler(event, context):
    # load fitted model
    key = key_template.format(id=event.get('modelId'), version=str(event.get('modelVersion')))
    tmp = '/tmp/{id}-{version}.pickle'.format(id=event.get('modelId'), version=str(event.get('modelVersion')))
    s3.Bucket(bucket).download_file(key, tmp)
    model_fitted = sm.load(tmp)
    # make prediction
    new_data   = event.get('data')
    prediction = model_fitted.predict(exog=new_data)
    result     = {
        'modelId': event.get('modelId'),
        'modelVersion': event.get('modelVersion'),
        'prediction': prediction[0]
    }
    return json.dumps(result)
