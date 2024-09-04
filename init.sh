#!/usr/bin/env bash
#
# Create a namespace for the app and install all associated resources.

# set -ex

# kind create cluster --config db.yaml
kubectl create ns myapp

pushd helm

### PostgreSQL ###
kubectl create -f postgres/passwords.secret.yaml
kubectl create -f postgres/postgres-pv.yaml
helm install postgres oci://registry-1.docker.io/bitnamicharts/postgresql \
  -n myapp --values postgres/values.yaml --wait --timeout 60s

### Traefik ###
helm install traefik oci://ghcr.io/traefik/helm/traefik \
  -n myapp --values traefik/values.yaml

### APIs ###
helm install test-api ./simple-service -n myapp --values test-api.yaml

# Delay for APIs to become available -- should replace with proper healthcheck
sleep 10

### Frontends ###
helm install frontend-main ./simple-service -n myapp --values frontend-main.yaml
helm install test-frontend ./simple-service -n myapp --values test-frontend.yaml
popd

# set +ex

. load_scripts.sh
db_expose
traefik_expose
web_expose
