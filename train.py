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

def load_native_libs(pack):
    deps_path = "/tmp/deps/" + pack.replace("-", "_")
    for lib in native_libs.get(pack, []):
        load(deps_path + "/lib/" + lib)

def load_pack(pack):
    pack_file = "/tmp/" + pack + ".zip"
    if os.path.isfile(pack_file):
        load_native_libs(pack)
        return

    s3 = boto3.resource('s3')
    s3.Bucket("ml-engineer").download_file(pack + ".zip", pack_file)

    zip_ref = zipfile.ZipFile(pack_file, 'r')
    deps_path = "/tmp/deps/" + pack.replace("-", "_")
    zip_ref.extractall(deps_path)
    zip_ref.close()
    sys.path.append(deps_path)

    load_native_libs(pack)

load_pack("sklearn-scipy-numpy")
load_pack("pandas-numpy-pack")
# ** End of ML Runtime **

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from sklearn.externals import joblib

feature_names = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
target_names = ['setosa', 'versicolor', 'virginica']

def train_classifier(iris):
    """Trains a model, returns a structure to persist"""

    df = pd.DataFrame(iris.data, columns=feature_names)
    df['species'] = pd.Categorical.from_codes(iris.target, target_names)
    df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75

    train_data = df[df['is_train']==True]
    y = pd.factorize(train_data['species'])[0]

    # Create a random forest Classifier. By convention, clf means 'Classifier'
    clf = RandomForestClassifier(n_jobs=2, random_state=0)

    # Train the Classifier to take the training features and learn how they relate
    # to the training y (the species)
    print clf.fit(train_data[feature_names], y)
    return clf

def store_model_to_s3(model, bucket, key):
    """Stores a model into S3 bucket 'ml-engineer' under the given key"""
    joblib.dump(model, "/tmp/model.pkl", compress=1)
    s3 = boto3.client('s3')
    s3.upload_file("/tmp/model.pkl", bucket, key)
    os.remove("/tmp/model.pkl")

def lambda_handler(event, context):
    """Entry point of training Lambda event execution"""

    np.random.seed(0)
    iris = load_iris()

    model = train_classifier(iris)

    store_model_to_s3(model, os.environ['STACK_NAME'], "model.pkl")

    return 'Model trained'
