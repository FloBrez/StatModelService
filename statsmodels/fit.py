from statsmodels.formula.api import ols
import boto3
import tempfile
import json
import os
import uuid
from pandas import DataFrame

bucket = os.environ['statsmodelsBucket']
key_template = os.environ['statsmodelsKeyTemplate']
s3 = boto3.resource('s3')

def lambda_handler(event, context):
    # fit model
    df = DataFrame(event.get('data'))
    model_fitted = ols(event.get('formula'), data=df).fit()
    print(model_fitted.summary())

    # save model (locally)
    version = str(uuid.uuid4())
    tmp = '/tmp/{id}-{version}.pickle'.format(id=event.get('modelId'), version=version)
    model_fitted.save(tmp, remove_data=True)

    # upload to S3
    key = key_template.format(id=event.get('modelId'), version=version)
    s3.Bucket(bucket).upload_file(tmp, key)

    # return model information
    df_parameters = DataFrame(
        data={
        'estimate': model_fitted.params,
        'se': model_fitted.bse,
        't': model_fitted.tvalues,
        'p': model_fitted.pvalues
    })

    parameters = df_parameters.to_dict(orient='index')

    #model_fitted.conf_int()
    #model_fitted.summary().as_text()
    #model_fitted.summary().as_html()

    result = {
        'modelId': event.get('modelId'),
        'modelVersion': version,
        's3bucket': bucket,
        's3key': key,
        'parameters': parameters
    }
    return json.dumps(result)



