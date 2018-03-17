import boto3
import zipfile
import sys
import os
from ctypes import cdll

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

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from sklearn.externals import joblib

def train(iris):
    """Trains a model, returns a structure to persist"""

    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
    df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75

    train_data, test_data = df[df['is_train']==True], df[df['is_train']==False]
    features = df.columns[:4]
    y = pd.factorize(train_data['species'])[0]

    # Create a random forest Classifier. By convention, clf means 'Classifier'
    clf = RandomForestClassifier(n_jobs=2, random_state=0)

    # Train the Classifier to take the training features and learn how they relate
    # to the training y (the species)
    print clf.fit(train_data[features], y)
    return [clf, test_data, features]

def store(model, s3_key):
    """Stores a model into S3 bucket 'ml-engineer' under the given key"""
    joblib.dump(model, "/tmp/model.pkl")
    s3 = boto3.client('s3')
    s3.upload_file("/tmp/model.pkl", "ml-engineer", s3_key)

def test(model, test_data, features, iris):
    """Tests a model, logs to Cloudwatch only for now"""
    print model.predict(test_data[features])
    print model.predict_proba(test_data[features])[0:10]

    preds = iris.target_names[model.predict(test_data[features])]
    print preds[0:5]
    print test_data['species'].head()

    print pd.crosstab(test_data['species'], preds, rownames=['Actual Species'], colnames=['Predicted Species'])

def lambda_handler(event, context):
    np.random.seed(0)
    iris = load_iris()

    model, test_data, features = train(iris)

    store(model, "models/" + os.environ['PARTICIPANT'] + "/model.pkl")

    test(model, test_data, features, iris)

    return 'Model trained'
