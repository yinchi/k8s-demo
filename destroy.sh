#!/usr/bin/env bash
#
# Uninstall all helm charts in the myapp namespace
# and delete the namespace
helm list -q -n myapp | xargs -I {} helm uninstall {} -n myapp
kubectl delete ns myapp
kubectl delete pv postgres-pv