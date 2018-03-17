#!/bin/bash

rm -rf out
mkdir out
zip out/train.zip train.py
zip out/predict.zip predict.py
