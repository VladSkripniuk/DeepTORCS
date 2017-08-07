#!/bin/sh
git clone https://github.com/tensorflow/tensorflow
cd tensorflow
printf "\n\n\n\n\n\n\n\n\n\n5" | ./configure
cp ../src/opencv.BUILD .
cat ../src/WORKSPACE  >> WORKSPACE
mkdir tensorflow/cc/driver
cp ../src/torcs_run* tensorflow/cc/driver
cp ../src/BUILD tensorflow/cc/driver
