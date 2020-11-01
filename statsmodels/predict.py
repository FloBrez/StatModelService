import statsmodels.api as sm
import boto3
import tempfile
import json
BUCKET    = 'code-janos'
MODEL_KEY = 'models/fitted_model.pickle'

s3  = boto3.resource('s3')
tmp = '/tmp/123.pickle'
s3.Bucket(BUCKET).download_file(MODEL_KEY, tmp)
MODEL_FITTED = sm.load(tmp)

def lambda_handler(event, context):
    new_data   = event # {'Region': 'E', 'Literacy': 65}
    prediction = MODEL_FITTED.predict(exog=new_data)
    result     = {'prediction': prediction[0]}
    return json.dumps(result)
