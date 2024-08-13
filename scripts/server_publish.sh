#!/usr/bin/env bash
#
# Pulls an image from the local Docker registry and publishes it to ghcr.io.
# Assumes that the local Docker registry is as http://localhost:5000, as specified
# in `scripts/local_registry.init.sh`.
#
# Usage: ./scripts/publish.sh image [source-tag="latest"] [dest-tag=source-tag]

echo "localhost:5000/myapp:${1:-latest} ==> ghcr.io/$GHCR_USER/myapp:${2:-${1:-latest}}"

docker pull localhost:5000/myapp:${1:-latest} && \
docker tag localhost:5000/myapp:${1:-latest} ghcr.io/$GHCR_USER/myapp:${2:-${1:-latest}} && \
docker push ghcr.io/$GHCR_USER/myapp:${2:-${1:-latest}}