#!/usr/bin/env bash
#
# List all images and tags in the local docker registry.
# The registry is assumed to be at http://localhost:5000,
# as specified in the `local_registry_init.sh` script.

curl -sX GET http://localhost:5000/v2/_catalog | \
jq '.repositories.[]' | \
xargs -I {} curl -X GET localhost:5000/v2/{}/tags/list