#!/usr/bin/env bash
#
# Uninstall all helm charts in the myapp namespace
# and delete the namespace

# Stop port-forwards
ps a | grep "kubectl port-forward -n myapp" | grep -v grep | awk '{print $1}' | xargs -n1 kill

# Uninstall helm charts
helm list -q -n myapp | xargs -I {} helm uninstall {} -n myapp

kubectl delete ns myapp
kubectl delete pv postgres-pv