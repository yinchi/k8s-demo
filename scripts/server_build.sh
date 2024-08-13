#!/usr/bin/env bash
#
# Build the `myapp` container.

pushd `git root`/myapp
docker build -t  localhost:5000/myapp --push .
popd