import urllib2
import boto3

def install_pack(url, s3_key):
    s3 = boto3.client('s3')
    response = urllib2.urlopen(url)
    s3.upload_fileobj(response, 'ml-engineer', s3_key)

def lambda_handler(event, context):
    install_pack("https://github.com/ryfeus/lambda-packs/raw/master/Pandas_numpy/Pack.zip", "pandas-numpy-pack.zip")
    install_pack("https://github.com/ryfeus/lambda-packs/raw/master/Sklearn_scipy_numpy/Pack.zip", "sklearn-scipy-numpy.zip")
