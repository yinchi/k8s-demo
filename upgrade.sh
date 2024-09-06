#!/usr/bin/env bash
#
# Force Kubernetes to restart the app's services, which will always pull the latest version from
# ghcr.io (assuming that the "latest" tag is used).

set -ex

### APIs ###
kubectl rollout restart deploy/myapp-test-api -n myapp

# Delay for APIs to become available -- should replace with proper healthcheck
sleep 10

### Frontends ###
kubectl rollout restart deploy/myapp-frontend-main -n myapp
kubectl rollout restart deploy/myapp-test-frontend -n myapp

set +ex
