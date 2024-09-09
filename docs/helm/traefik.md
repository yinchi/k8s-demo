# Traefik setup

Our Traefik setup is largely based off of [this](https://traefik.io/blog/getting-started-with-kubernetes-gateway-api-and-traefik/) official Traefik blog post.  The values file for our Traefik service is at `helm/values/traefik.md`:

```yaml
providers:
  # Disable the Ingress provider (optional)
  # We do not want to use Ingress objects anymore!
  kubernetesIngress:
    enabled: false
  # Enable the GatewayAPI provider
  kubernetesGateway:
    enabled: true
ingressRoute:
  dashboard:
    enabled: true
```

Unlike the example from the official blog, we will only expose routes from the `myapp` namespace; thus we will use the default `gateway.namespacePolicy` value.

The following excerpt from `init.sh` installs the chart:

```bash
helm upgrade -i traefik \
  oci://ghcr.io/traefik/helm/traefik \
  -n myapp \
  --values values/traefik.yaml
```

Check our configuration:

```console
$ kubectl describe svc traefik | grep ^Port: -A3
Port:                     web  80/TCP
TargetPort:               web/TCP
NodePort:                 web  30884/TCP
Endpoints:                10.244.0.21:8000
Port:                     websecure  443/TCP
TargetPort:               websecure/TCP
NodePort:                 websecure  30971/TCP
Endpoints:                10.244.0.21:8443
$ kubectl describe deploy traefik | grep -i entrypoint
      --entryPoints.metrics.address=:9100/tcp
      --entryPoints.traefik.address=:9000/tcp
      --entryPoints.web.address=:8000/tcp
      --entryPoints.websecure.address=:8443/tcp
      --metrics.prometheus.entrypoint=metrics
      --entryPoints.websecure.http.tls=true
```

Finally, we expose the `web` (for our webapp) and `traefik` (for the admin dashboard) endpoints. The corresponding lines from `init.sh` are:

```bash
. load_scripts.sh
traefik_expose
web_expose
```

```{figure} ../_images/traefik_dashboard.png
:alt: Screenshot of the Traefik dashboard

Screenshot of the Traefik dashboard exposed on `localhost:9000`.
```

## HTTPRoute and Middlewares

The directory `helm/charts/simple-service/` demonstrates how to create a `HTTPRoute` to Traefik.  The three template files create a `Deployment`, `Service`, and `HTTPRoute`.  The specification for the `HTTPRoute` contains the following:

```bash
helm template test charts/simple-service/ --values values/test/api.yaml | \
yq 'select(.kind == "HTTPRoute").spec.rules'
```

```yaml
- matches:
    - path:
        type: PathPrefix
        value: /test-module/api
  backendRefs:
    - name: myapp-test-api
      namespace: myapp
      port: 3000
  filters:
    - type: ExtensionRef
      extensionRef:
        group: traefik.io
        kind: Middleware
        name: strip-prefix-test-api
```

```bash
helm template test charts/simple-service/ --values values/test/api.yaml | \
yq 'select(.kind == "Middleware")'
```

```yaml
# Source: simple-service/templates/03-traefik.yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: strip-prefix-test-api
  namespace: myapp
spec:
  stripPrefix:
    prefixes:
      - /test-module/api
```

This instructs Traefik to forward requests containing the path prefix `/test-module/api` to the `myapp-test-api` service in the `myapp` namespace on port `3000`, after applying the `strip-prefix-test-api` Middleware, which strips the path prefix from the forwarded request.  Note that the `ExtensionRef` filter and `Middleware` are only included in our Helm chart if `traefik.stripPrefix` is set to `true` in our values file.