import boto3
import zipfile
import sys
import os
from ctypes import cdll

# ** Start of ML Runtime **
# Don't edit :)
native_libs = {
    "sklearn-scipy-numpy":
    ["libquadmath.so.0",
     "libgfortran.so.3",
     "libatlas.so.3",
     "libptcblas.so.3",
     "libptf77blas.so.3",
     "libf77blas.so.3",
     "libcblas.so.3",
     "liblapack.so.3"]
}

def load(lib):
    print "loading " + lib
    cdll.LoadLibrary(lib)

def load_pack(pack):
    pack_file = "/tmp/" + pack + ".zip"
    if os.path.isfile(pack_file):
        return

    s3 = boto3.resource('s3')
    s3.Bucket("ml-engineer").download_file(pack + ".zip", pack_file)

    zip_ref = zipfile.ZipFile(pack_file, 'r')
    deps_path = "/tmp/deps/" + pack.replace("-", "_")
    zip_ref.extractall(deps_path)
    zip_ref.close()
    sys.path.append(deps_path)

    for lib in native_libs.get(pack, []):
        load(deps_path + "/lib/" + lib)

load_pack("sklearn-scipy-numpy")
load_pack("pandas-numpy-pack")

# ** End of ML Runtime **

import pandas as pd
import numpy as np
from sklearn.externals import joblib

feature_names = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
target_names = ['setosa', 'versicolor', 'virginica']

def fetch_model(s3_key_prefix):
    trained_model_file = "/tmp/trained-model.pkl"
    s3 = boto3.resource('s3')
    s3.Bucket("ml-engineer").download_file(s3_key_prefix + "model.pkl", trained_model_file)
    return joblib.load(trained_model_file)

def predict(model, params):
    df = pd.DataFrame(data = [[params["sepal_length"],
                               params["sepal_width"],
                               params["petal_length"],
                               params["petal_width"]]],
                      columns=feature_names)
    return np.array(target_names)[model.predict(df)]

def lambda_handler(event, context):
    np.random.seed(0)

    model = fetch_model("models/" + os.environ['PARTICIPANT'] + "/")
    result = predict(model, event['queryStringParameters'])
    return {"statusCode": 200,
            "isBase64Encoded": False,
            "body": str(result)}
