# Machine Learning Engineer Programme - Exercise 4

1. Login to AWS
  * For Solita sandbox login, see: <link to intra>
2. Create Cloudformation stack by using: https://s3-eu-west-1.amazonaws.com/ml-engineer/cloudformation/ml-stack.yml
  * Name the stack as `mle4-<username>`
  * This will create the following resources:
    * Two Lambda functions
      * `mle4-<username>-train` for training the model
      * `mle4-<username>-predict` for using a trained model for prediction
    * API Gateway REST API named `mle4-<username>`
      * With `/` route mapped to `mle4-<username>-predict` Lambda
3. Train the example model by running `mle4-<username>-train` Lambda
  * Configure test event:
  ```
  {"queryStringParameters":
    {"sepal_length": 1,
     "sepal_width": 1,
     "petal_length": 1,
     "petal_width": 1}}
  ```
4. Test the sample API Gateway
  * Select `GET` method of `/` resource
  * Press `Test` and pass query string: `?sepal_length=1&sepal_width=1&petal_length=1&petal_width=1`
5. Deploy the sample API
  * Click `Actions`, select `Deploy API`
  * Create new stage named `dev` and click `Deploy`
  * Browse to the URL, pass query string
6. Plug your own algorithm and model
7. Test it
8. Deploy and share to #ml-engineer
