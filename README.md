# DeepTORCS

This repository contains adaptation of [DeepDriving](http://deepdriving.cs.princeton.edu/) project for Tensorflow in addition to some supplementary scripts for training, evaluating and visualizing Convolutional Network used for driving.

## Data

The original training and test data can be downloaded from [DeepDriving](http://deepdriving.cs.princeton.edu/) website.

```
wget http://deepdriving.cs.princeton.edu/TORCS_trainset.zip # 50GB
wget http://deepdriving.cs.princeton.edu/TORCS_baseline_testset.zip # 8GB
```

Original training data was recorded from 12 hours of human driving in TORCS video game and contains 484815 entries in LevelDB format. Each entry is a screenshot from the game and 14 numbers describing current road scene. ([Original article](http://deepdriving.cs.princeton.edu/paper.pdf) mysteriously describes only 13 numbers)

![TORCS screenshot](https://github.com/skripniuk/DeepTORCS/blob/master/pictures/screenshot.jpg)

To train a CNN in Tensorflow this data can be converted from LevelDB to TFRecords using ```leveldb2tfrecords.py``` script. This script depends on [Caffe](http://caffe.berkeleyvision.org/), so it could be launched inside [Caffe docker](https://hub.docker.com/r/bvlc/caffe/).

## Model

The CNN given an image should predict 14 numbers, next steering command is computed based on those numbers . All targets are rescaled to [0..1], so that Euclidean L2 loss can be used for training. We trained AlexNet and MobileNet architectures with modified number of outputs:

![Learning curves](https://github.com/skripniuk/DeepTORCS/blob/master/pictures/curves.png)

## Visualization

To visualize, what CNN has learned, one can highlight parts of image, which influence the output of the network at most. For instance, one can compute the gradient of network output with respect to an input image. To generate the picture below, we've computed the gradient of the output node, which predicts distance to car ahead in the current lane, and highlighted each pixel in proportion to the magnitude of the gradient.

![Attention](https://github.com/skripniuk/DeepTORCS/blob/master/pictures/attention.png)
