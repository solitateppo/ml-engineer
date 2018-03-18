# Machine Learning Engineer Programme - Exercise 4

1. Login to Solita AWS Sandbox
2. Create Cloudformation stack by using: https://s3-eu-west-1.amazonaws.com/ml-engineer/cloudformation/ml-stack.yml
  * Name the stack as `mle4-<username>`
  * This will create the following resources:
    * Two Lambda functions
      * `mle4-<username>-train` for training the model
      * `mle4-<username>-predict` for using a trained model for prediction
    * API Gateway REST API named `mle4-<username>`
      * With `/` route mapped to `mle4-<username>-predict` Lambda
3. Train the example model by running `mle4-<username>-train` Lambda
4. Test the sample API Gateway
5. Plug your own algorithm and model
6. Test it
7. Deploy and share to #ml-engineer
