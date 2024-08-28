#!/usr/bin/env bash
#
# Create a namespace for the app and install all associated resources.

set -ex

### APIs ###
kubectl rollout restart deploy/myapp-test-api -n myapp

# Delay for APIs to become available -- should replace with proper healthcheck
sleep 10

### Frontends ###
kubectl rollout restart deploy/myapp-frontend-main -n myapp
kubectl rollout restart deploy/myapp-test-frontend -n myapp

set +ex
