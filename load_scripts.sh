#! /bin/sed 2,5!d;s/^#.//
# This script must be sourced from within a shell
# and not executed. For instance with:
# 
#   . path/to/this/script
#
# Add the scripts directory to the system path and sets some environment variables.

export PATH=`git root`/scripts:$PATH

# Get the github user/org from the remote git URL, e.g. 'yinchi' for
# 'https://github.com/yinchi/...'. The matching repository URL prefix is 'ghcr.io/yinchi/...'.
export GHCR_USER=$(git remote get-url origin | cut -d'/' -f4)

echo "Added $(git root) to PATH"
echo "Set GHCR_USER to $GHCR_USER"
echo "Set MYAPP to myapp"

alias popy="poetry run python"
alias polint="poetry run pylint --rcfile=`git root`/.pylintrc"
