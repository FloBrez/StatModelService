import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import boto3
import tempfile
import json
BUCKET    = 'code-janos'
MODEL_KEY = 'models/fitted_model.pickle'

# Input
data = [
    {'Region': 'E', 'Literacy': 55,  'Pop1831': 344.21}, 
    {'Region': 'W', 'Literacy': 35,  'Pop1831': 111.21}, 
    {'Region': 'S', 'Literacy': 105, 'Pop1831': 89.21},
    {'Region': 'C', 'Literacy': 105, 'Pop1831': 33.21},
    {'Region': 'W', 'Literacy': 45,  'Pop1831': 121.21}, 
    {'Region': 'S', 'Literacy': 85,  'Pop1831': 45.31},
    {'Region': 'C', 'Literacy': 15, 'Pop1831':  10.21},
    {'Region': 'N', 'Literacy': 33,  'Pop1831': 78.21}
]
formula = 'Pop1831 ~ Literacy + Region'

# Data Preparation
df = pd.DataFrame(data)

# Model Fit
model_fitted  = smf.ols(formula, data=df).fit()
model_fitted.summary().as_csv()
print(model_fitted.summary())
model_fitted.save('fitted_model.pickle', remove_data=True)
model_fitted.rsquared
# Save Data
s3  = boto3.resource('s3')
tmp = '/tmp/123.pickle'
s3.Bucket(BUCKET).download_file(MODEL_KEY, tmp)
MODEL_FITTED = sm.load(tmp)

x = pd.DataFrame(data={
    'estimate': model_fitted.params,
    'se': model_fitted.bse,
    't': model_fitted.tvalues,
    'p': model_fitted.pvalues
})

x.to_dict(orient='index')

model_fitted.conf_int()
model_fitted.summary().as_text()
model_fitted.summary().as_html()




