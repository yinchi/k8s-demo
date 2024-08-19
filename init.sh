#!/usr/bin/env bash
#
# Create a namespace for the app and install all associated resources.

# kind create cluster --config db.yaml
kubectl create ns myapp

pushd helm

### PostgreSQL ###
kubectl create -f postgres/passwords.secret.yaml
kubectl create -f postgres/postgres-pv.yaml
helm install postgres oci://registry-1.docker.io/bitnamicharts/postgresql \
  -n myapp --values postgres/values.yaml --wait --timeout 60s

### API (Deployment) ###
helm install myapp-api ./simple-service -n myapp --values values-api.yaml
helm install myapp-frontend ./simple-service -n myapp --values values-frontend.yaml
popd