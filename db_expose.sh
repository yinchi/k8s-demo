#! /bin/sed 2,5!d;s/^#.//
# This script must be sourced from within a shell
# and not executed. For instance with:
# 
#   . path/to/this/script
#
# Expose the postgresql database to the host machine.

kubectl port-forward -n myapp svc/postgres --address 0.0.0.0 5432:5432 &> /dev/null &