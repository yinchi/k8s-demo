#! /bin/sed 2,5!d;s/^#.//
# This script must be sourced from within a shell
# and not executed. For instance with:
# 
#   . path/to/this/script
export PATH=`git root`/scripts:$PATH
alias server_docker="docker run --rm -it --network=kind -p 0.0.0.0:80:80 -e postgres_host='172.18.0.1' --name=myapp localhost:5000/myapp"