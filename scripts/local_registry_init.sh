#!/usr/bin/env bash
#
# Create a local docker registry at http://localhost:5000.
#
# To remove the registry, use
#    docker stop registry && docker rm -v registry

docker run -d -p 5000:5000 --restart always --name registry registry:2.8.3