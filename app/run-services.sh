#!/bin/bash

# move to app directory
cd $PROJECT

# Copy credentials.txt to TwitterAPI module
cp $PROJECT/assets/TwitterAPI/credentials.txt   /usr/local/lib/python2.7/dist-packages/TwitterAPI/

# show $PROJECT directory at CONTAINER-IP:9091
nohup python -m SimpleHTTPServer 9091 &> /dev/null &

# list all processes
ps -eu

# run app
python $PROJECT/scripts/TwitterStream.py

