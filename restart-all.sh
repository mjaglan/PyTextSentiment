#!/bin/bash

# variables
IMG_NAME="mjaglan/pytextsentiment"
HOST_NAME="testbed"
NETWORK_NAME=$HOST_NAME

# if desired, clean up containers
docker stop $(docker ps -a -q)
docker rm -v $(docker ps -a -q)

# if desired, clean up images
if [[ "$1" == "rmi" ]] ; then
	docker rmi $(docker images -q)
fi

# build the Dockerfile
docker build  -t "$IMG_NAME" "$(pwd)"

# Default docker network name is 'bridge', driver is 'bridge', scope is 'local'
# Create a new network with any name, and keep 'bridge' driver for 'local' scope.
NET_QUERY=$(docker network ls | grep -i $NETWORK_NAME)
if [ -z "$NET_QUERY" ]; then
	echo "Create network >>> $NETWORK_NAME"
	docker network create --driver=bridge $NETWORK_NAME
fi

# start python web application
docker run --name "$HOST_NAME" -h "$HOST_NAME" --net=$NETWORK_NAME \
		-v  $(pwd)/app:/tmp/app \
		-p  9091:9091 \
		-itd "$IMG_NAME"

# see active docker containers
docker ps

# start application service
MY_CMD="/tmp/app/run-services.sh"
docker exec -it $HOST_NAME $MY_CMD

# attach to the container
docker attach "$HOST_NAME"
