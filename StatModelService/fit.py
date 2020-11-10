from statsmodels.formula.api import ols
import boto3
import json
import os
import uuid
from pandas import DataFrame

bucket       = os.environ['bucket']
key_template = os.environ['keyTemplate']
s3 = boto3.resource('s3')

def fit_model(data, formula):
    df = DataFrame(data)
    model_fitted = ols(formula, data=df).fit()
    return model_fitted

def save_model(model):
    model_id = str(uuid.uuid4())
    tmp = '/tmp/{id}.pickle'.format(id=model_id)
    model.save(tmp, remove_data=True)
    key = key_template.format(id=model_id)
    response = s3.Bucket(bucket).upload_file(tmp, key)
    return {"model_id": model_id, "s3_response": response}

def collect_model_info(model):
    df_parameters = DataFrame(
        data={
        'estimate': model.params,
        'se': model.bse,
        't': model.tvalues,
        'p': model.pvalues
    })
    parameters = df_parameters.to_dict(orient='index')
    #model_fitted.conf_int()
    #model_fitted.summary().as_text()
    #model_fitted.summary().as_html()
    return parameters

def lambda_handler(event, context):
    payload = json.loads(event['body'])
    model = fit_model(data = payload['data'], formula = payload['formula'])
    print(model.summary())
    save_response = save_model(model=model)
    model_info = collect_model_info(model=model)

    result = {
        'modelId': save_response['model_id'],
        'modelInfo': model_info
    }

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }