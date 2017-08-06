#!/bin/sh
git clone https://github.com/tensorflow/tensorflow
cd tensorflow
./configure
cp ../src/opencv.BUILD .
echo ../src/WORKSPACE  >> WORKSPACE
mkdir tensorflow/cc/driver
cp ../src/torcs_run* tensorflow/cc/driver
cp ../src/BUILD tensorflow/cc/driver
