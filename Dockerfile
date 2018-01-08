# author mjaglan@umail.iu.edu
# Coding Style: Shell form

# Start from Ubuntu OS image
FROM ubuntu:14.04

# set root user
USER root

# install utilities on up-to-date node
# scikit-learn: http://scikit-learn.org/0.16/_sources/install.txt
RUN apt-get update && apt-get -y dist-upgrade && apt-get -y install -f \
	&& apt-get -y install python python-pip python-dev build-essential \
	python-setuptools python-numpy python-scipy libatlas-dev libatlas3gf-base \
	python-sklearn

# upgrade python2 requests package
RUN pip install --upgrade requests

# pip packages
# TwitterAPI: https://github.com/geduldig/TwitterAPI
RUN pip install TwitterAPI \
				microsofttranslator \ 
				nltk

# Download NLTK Data
RUN python -m nltk.downloader all

# Create PROJECT directory
RUN mkdir /tmp/app/

# Set Project HOME
ENV PROJECT=/tmp/app/

# Set active working directory
WORKDIR $PROJECT

# Start process
ENTRYPOINT bash
