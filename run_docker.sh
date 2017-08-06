#!/bin/sh
COMMAND=/bin/bash

# allow connections to X server
xhost +local:docker

SHARED_DIR = $(pwd)

nvidia-docker run --privileged -e "DISPLAY=unix:0.0" -v="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v="${SHARED_DIR}:/shared" -p 7777:7777 -i -t deep_torcs $COMMAND