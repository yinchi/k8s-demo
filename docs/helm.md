# Helm charts

Helm charts are defined in the `helm/charts` directory, while custom values for our app are located in `helm/values`.  Our `init.sh` script contains commands for installing each Helm chart in our app. For example, to install Traefik:

```bash
helm upgrade -i traefik \
  oci://ghcr.io/traefik/helm/traefik \
  -n myapp \
  --values values/traefik.yaml
```

To install a first-party chart, e.g. `simple-service`:

```bash
helm upgrade -i test-api \
  ./charts/simple-service \
  -n myapp \
  --values values/test/api.yaml
```