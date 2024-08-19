#! /bin/sed 2,5!d;s/^#.//
# This script must be sourced from within a shell
# and not executed. For instance with:
# 
#   . path/to/this/script
#
# Add the scripts directory to the system path and sets some environment variables.

echo `prepend_path scripts/`
export `prepend_path scripts/`

alias popy="poetry run python"
alias polint="poetry run pylint --rcfile=`git root`/.pylintrc"

alias db_expose="screen -dmS myapp-postgres-portfwd kubectl port-forward -n myapp svc/postgres --address 0.0.0.0 5432:5432 &"

alias api_expose="screen -dmS myapp-api-portfwd kubectl port-forward -n myapp svc/myapp-api --address 0.0.0.0 3000:3000"

alias frontend_expose="screen -dmS myapp-frontend-portfwd kubectl port-forward -n myapp svc/myapp-frontend --address 0.0.0.0 8080:8080"