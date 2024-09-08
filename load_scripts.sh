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

alias traefik_expose="screen -dmS traefik-dash-portfwd kubectl port-forward -n myapp deploy/traefik 9000:traefik &"
alias web_expose="screen -dmS myapp-portfwd kubectl port-forward -n myapp svc/traefik 8000:web &"

alias k="kubectl"
alias pods="kubectl get pods -n myapp"
alias logs="kubectl logs -n myapp"

ns () {
    kubectl config set-context --current --namespace=$@
}