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

Test MAE of AlexNet after 140k iterations:

| Parameter  | angle | to_LL | to_ML | to_MR | to_MR | to_L | to_M | to_R | dist_L | dist_R | dist_LL | dist_MM | dist_RR |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| Test MAE | 0.040  | 0.172 | 0.237 | 0.219 | 0.234 | 0.168 | 0.254 | 0.207 | 1.629 | 1.800 | 1.895 | 2.101 | 2.348 |


## Visualization

To visualize, what CNN has learned, one can highlight parts of image, which influence the output of the network at most. For instance, one can compute the gradient of network output with respect to an input image. To generate the picture below, we've computed the gradient of the output node, which predicts distance to car ahead in the current lane, and highlighted each pixel in proportion to the magnitude of the gradient.

![Attention](https://github.com/skripniuk/DeepTORCS/blob/master/pictures/attention.png)

## How to launch CNN training
Jupyter notebooks for training and evaluating are gathered in ```notebooks``` subfolder:

```net.ipynb``` - CNN training

```evaluate.ipynb``` - CNN evaluation on test data

```progress.ipynb``` - visualize current loss

```attention.ipynb``` - visualize most influential parts of image

## How to launch autonomous driving
This code can be launched on a computer with NVidia graphics card and installed NVidia driver. You should download TORCS sources and modified tracks (```torcs-1.3.6``` and ```modified_tracks``` from [DeepDriving](http://deepdriving.cs.princeton.edu/DeepDrivingCode_v2.zip)) into this repository.

The code should be launched inside Docker container, so that you don't have to resolve dependencies. ```Dockerfile``` is provided, one can build an image with ```build_docker_image.sh```. After image is built, container can be launched with ```run_docker.sh```.

Following steps should be launched inside Docker container.

To build driver with Tensorflow, one have to download Tensorflow sources with ``get_TF.sh````.

After that, one should come into tensorflow folder, and build corresponding version of driver with:

```bazel build --config=opt --config=cuda //tensorflow/cc/driver:drive_3lane```

Next, one should launch ```torcs```, configure players, start quick race and remove extra elements from the screen in accordance to [README](https://github.com/skripniuk/DeepTORCS/blob/master/Readme) of the original DeepDriving.

Finally, driver can be launched with 

```./bazel-bin/tensorflow/cc/driver/drive_3lane```

and started in accordance to [README](https://github.com/skripniuk/DeepTORCS/blob/master/Readme) of the original DeepDriving.
