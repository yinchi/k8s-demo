#! /bin/sed 2,5!d;s/^#.//
# This script must be sourced from within a shell
# and not executed. For instance with:
# 
#   . path/to/this/script
#
# Add the scripts directory to the system path and sets some environment variables.

echo PATH=\"$(echo `prepend_path scripts/`)\"
export PATH=$(echo `prepend_path scripts/`)

alias popy="poetry run python"
alias polint="poetry run pylint --rcfile=`git root`/.pylintrc"

alias db_expose="screen -dmS myapp-postgres-portfwd kubectl port-forward -n myapp svc/postgres0 --address 0.0.0.0 5432:5432 &"
alias traefik_expose="screen -dmS traefik-dash-portfwd kubectl port-forward -n myapp $(kubectl get pods --selector "app.kubernetes.io/name=traefik" --output=name -n myapp) 9000:9000 &"
alias web_expose="screen -dmS myapp-portfwd kubectl port-forward -n myapp $(kubectl get pods --selector "app.kubernetes.io/name=traefik" --output=name -n myapp) 8000:8000 &"
