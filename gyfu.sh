#!/bin/bash

TAG=0.1
NO_CACHE="false"

# requires a docker-container buildx driver
BUILD_OPTIONS="--platform linux/arm64/v8,linux/amd64 --push"
if [ "$NO_CACHE" = true ]; then
    BUILD_OPTIONS+=" --no-cache=true"
    echo "building without cache"
else
    echo "building with cache"
fi

docker buildx build $BUILD_OPTIONS -t josiahdc/echo_runner:"${TAG}" ./echo_runner
docker buildx build $BUILD_OPTIONS -t josiahdc/errand_runner:"${TAG}" ./errand_runner
