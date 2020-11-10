# StatModelService
A simple way to create and use statistical models using serverless resources and a web API on AWS.

StatModelService uses AWS Lambda with Python 3.8 runtime to fit statistical models using Python's `statmodels` package. The current implementation only allows to fit models using ordinary least squares (OLS), but allows to define models using the convenient model formulas familiar from `R`. Each fitted model is saved to S3 (without data) and is readily available for predictions. Both, model creation and predicting new observations is available via HTTP requests, so you can easily integrate it with any other programming language or service.

![Architecture](/StatModelServiceArchitecture.png)


TODO: elaborate on goal, high-level design

## Installation
You can install StatModelService in your AWS account using [AWS serverless application model (SAM)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html). All resources are defined in `template.yaml` and deployment information is defined in `samconfig.toml`. In the latter, make sure to adjust the `region` parameter (default is `eu-central-1`) and add/delete custom `tags` for the deployment.

Using the SAM CLI to build and deploy the service reduced to two commands
```
sam build
```
will package the Python scripts in `StatModelService` folder and the dependencies in `requirements.txt`.

A guided deployment can be started with 
```
sam deploy --guided
```

## Usage
As the service is accessible via web API, you can define and fit/train models using any client and programming language that can send HTTP requests. Since the implementation is serverless, you do not have to maintain servers and the service scales easily and cost-effectively.  

### Example
To define and fit/train a statistical model, you send a POST request to your API's `/fit` path. The payload consists of the model formula (in R notation) and the data (in JSON format). To evaluate a simple A/B test with numerical outcome you would send data like this:
```json 
{
	"formula": "Outcome ~ Treatment",
	"data": [
		{"Treatment": "A", "Outcome": 110}, 
		{"Treatment": "A", "Outcome": 90}, 
		{"Treatment": "A", "Outcome": 120},
		{"Treatment": "A", "Outcome": 80},
		{"Treatment": "A", "Outcome": 100},
		{"Treatment": "B", "Outcome": 70}, 
		{"Treatment": "B", "Outcome": 110},
		{"Treatment": "B", "Outcome": 100},
		{"Treatment": "B", "Outcome": 80},
		{"Treatment": "B", "Outcome": 90}
	]
}
```
The response you receive contains a model Id, a unique identifier for your fitted model, and some basic model information, including the parameter point estimates, their standard error, t-statistics and p-values:
```json
{
    "modelId": "c73a00ff-2a3e-444f-baa6-99834812bd3a",
    "modelInfo": {
        "Intercept": {
            "estimate": 100.00000000000001,
            "se": 7.0710678118654755,
            "t": 14.142135623730953,
            "p": 6.077960694342541e-07
        },
        "Treatment[T.B]": {
            "estimate": -9.999999999999993,
            "se": 10.000000000000004,
            "t": -0.9999999999999989,
            "p": 0.34659350708733455
        }
    }
}
```

If you wanted to further use the model to predict outcomes for new observations, you can do this by sending a POST request to the `/predict` path of the API. The payload consists of the model Id and the data (again in JSON format) 
```json 
{
	"modelId": "c73a00ff-2a3e-444f-baa6-99834812bd3a",
	"data": {"Treatment": "A"}
}
```
Note, that `data` is a map/dict, not an array, since the code is expected to process one new observation at a time.

The response (body) just contains the predicted value
```json
{
    "prediction": 100.00000000000001
}
```

## FAQ
TODO:
