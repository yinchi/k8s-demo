#!/usr/bin/env bash
#
# Remove the local docker registry, assumed to be a Docker container on the local host
# named `registry`.

docker stop registry && docker rm -v registry