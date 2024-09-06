#!/usr/bin/env bash
#
# Create a namespace for the app and install all associated resources.

pushd src
docker compose build --push
popd

# kind create cluster --config kind.yaml
kubectl create ns myapp

pushd helm

### PostgreSQL ###
helm upgrade -i postgres0-additional \
   ./charts/postgres-additional \
  -n myapp \
  --values values/postgres0/pvc.yaml --values values/postgres0/secret.yaml

helm upgrade -i postgres0 \
  oci://registry-1.docker.io/bitnamicharts/postgresql \
  -n myapp \
  --values values/postgres0/main.yaml \
  --wait --timeout 60s

### Traefik ###
helm upgrade -i traefik \
  oci://ghcr.io/traefik/helm/traefik \
  -n myapp \
  --values values/traefik.yaml

### APIs ###
helm upgrade -i test-api \
  ./charts/simple-service \
  -n myapp \
  --values values/test/api.yaml

# Delay for APIs to become available -- should replace with proper healthcheck
sleep 10

### Frontends ###
helm upgrade -i frontend-main \
  ./charts/simple-service \
  -n myapp \
  --values values/frontend-main.yaml

helm upgrade -i test-frontend \
  ./charts/simple-service \
  -n myapp \
  --values values/test/frontend.yaml

popd

. load_scripts.sh
traefik_expose
web_expose
