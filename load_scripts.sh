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

# Start a local Docker container registry at http://localhost:5000.
registry_start() {
    docker run --rm -d -p 5000:5000 --restart always \
    --name registry registry:latest
}

# List images on the Docker container registry at http://localhost:5000.
registry_ls() {
    curl -sX GET http://localhost:5000/v2/_catalog | \
    jq '.repositories.[]' | \
    xargs -I {} curl -X GET localhost:5000/v2/{}/tags/list
}

# Push local images to the Docker container registry at http://localhost:5000.
# All images matching "localhost:5000/myapp[...]:latest" are pushed.
registry_push() {
    docker images --format '{{.Repository}}:{{.Tag}}' | grep "localhost:5000/myapp" | \
    grep ":latest" | xargs -I {} docker push {}
}

# Start a local pypi registry at http://localhost:31415. Because pi.
pypidev_start() {
    docker run --rm -d -p 31415:8080 -v $HOME/pypackages:/data/packages \
    --name pypiserver pypiserver/pypiserver:latest run
}
