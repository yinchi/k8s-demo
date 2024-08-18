#!/usr/bin/env bash
#
# Create a namespace for the app and install all associated resources.

# kind create cluster --config db.yaml
kubectl create ns myapp

### PostgreSQL ###

pushd postgres
kubectl create -f passwords.secret.yaml
kubectl create -f postgres-pv.yaml
helm install postgres oci://registry-1.docker.io/bitnamicharts/postgresql \
  -n myapp --values values.yaml --wait --timeout 60s
popd


### API (Deployment) ###

pushd myapp-k8s
kubectl apply -f myapp-api.yaml
popd