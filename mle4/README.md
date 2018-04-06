# Machine Learning Engineer Programme - Exercise 4

Task 1 is about using AWS, task 2 is a study on compute environment in AWS.

## Task 1

Use AWS Lambda for running the model (train and predict) created in previous exercise (task 1. might be more amenable).

1. Login to AWS
  * For Solita sandbox login, see: https://intra.solita.fi/display/RJO/Solita+AWS+Sandbox+login
  * Change to Ireland region (`eu-west-1`, console will remember this after first login) 
![image](https://user-images.githubusercontent.com/57011/38420366-206bb5da-39ac-11e8-902f-553ddef3ed5f.png)
2. Create Cloudformation stack by using: https://s3-eu-west-1.amazonaws.com/ml-engineer/cloudformation/ml-stack.yml
  * Name the stack as `mle4-<username>`
  * This will create the following resources:
    * Two Lambda functions
      * `mle4-<username>-train` for training the model
      * `mle4-<username>-predict` for using a trained model for prediction
    * API Gateway REST API named `mle4-<username>`
      * With `/` route mapped to `mle4-<username>-predict` Lambda
3. Train the example model by running `mle4-<username>-train` Lambda
4. Test the example model by running `mle4-<username>-predict` Lambda
  * Configure a test event:
  ```
  {"queryStringParameters":
    {"sepal_length": 1,
     "sepal_width": 1,
     "petal_length": 1,
     "petal_width": 1}}
  ```
5. Test the sample API Gateway
  * Select `GET` method of `/` resource
  * Press `Test` and pass query string: `?sepal_length=1&sepal_width=1&petal_length=1&petal_width=1`
6. Deploy the sample API
  * Click `Actions`, select `Deploy API`
  * Create new stage named `dev` and click `Deploy`
  * Browse to the URL, pass query string
7. Plug your own algorithm and model
8. Test it
9. Deploy and share link to the API to Slack

## Task 2

Study machine learning compute environments available in AWS. This might be a good time to look into Sagemaker service,
if you'r not already familiar with it: https://aws.amazon.com/sagemaker/

If you also try out AWS services, it's a good idea to tag the resources with `project: ml-engineer`.

Idea is to discuss about the compute environments in the exercise meeting on 27.4.2018.
