#!/usr/bin/env bash
#
# Run the `myapp` server in docker. The connection to the postgresql
# server is via the `kind` bridge network, with the host machine acting
# as a gateway.
#
# Use `kubectl port-forward` to forward port 5432 on the postgresql server to
# port 5432 on the host machine, which the `myapp` container can reach via
# the bridge network.

# Get IP address of host on `kind` network
# Use `jq -r` to unquote string
GATEWAY=$(docker inspect kind | \
jq -r '.[].IPAM.Config.[].Gateway' | grep "172" | head -n 1)

echo "Gateway is $GATEWAY"

# Launch container
docker run --rm -it --network=kind -p 0.0.0.0:80:80 \
-e postgres_host="$GATEWAY" \
--name=myapp localhost:5000/myapp