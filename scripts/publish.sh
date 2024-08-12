#!/usr/bin/env bash
#
# Pulls an image from the local Docker registry and publishes it to ghcr.io.
# Assumes that the local Docker registry is as http://localhost:5000, as specified
# in `scripts/local_registry.init.sh`.
#
# Usage: ./scripts/publish.sh image [source-tag="latest"] [dest-tag=source-tag]

if [ -z "${GHCR_USER-}" ]; then
    echo "GHCR_USER unset or empty, exiting."
    exit 127
fi

echo "localhost:5000/$1:${2:-latest} ==> ghcr.io/$GHCR_USER/$1:${3:-${2:-latest}}"

docker pull localhost:5000/$1:${2:-latest} && \
docker tag localhost:5000/$1:${2:-latest} ghcr.io/$GHCR_USER/$1:${3:-${2:-latest}} && \
docker push ghcr.io/$GHCR_USER/$1:${3:-${2:-latest}}