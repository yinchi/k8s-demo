# The `simple-service` Chart

The `simple-service` chart contains a Deployment, a Service linked to this Deployment, and an HTTPRoute for adding the Service to Traefik.

## Values

```{list-table}
:header-rows: 1

* - Name
  - Description
  - Value
* - app.name
  - Name to apply to the created resources.
  - xxx
* - app.container.image
  - Docker image tag for the created Pod.
  - ghcr.io/yinchi/myapp-xxx:latest
* - app.container.port
  - Port number to expose.
  - 8000
* - app.container.env
  - List of environment variables, e.g
    ```yaml
      - name: var1
        value: val1
      - name: var2
        value: val2 
    ```
  - []
* - app.container.secretenv
  - List of environment variables associated with Secrets, e.g
    ```yaml
      - name: secretVar1
        secretName: mySecret
        key: key1
      - name: secretVar2
        secretName: mySecret
        key: key2
    ```
  - []
* - service.type
  - The Service type, one of "ClusterIP", "NodePort", "LoadBalancer", or "ExternalName"
  - ClusterIP
* - service.protocol
  - The protocol used by the Service, one of TCP, UDP, or SCTP.
  - TCP
* - service.port
  - The port number to expose the service on.
  - 3000
* - traefik.stripPrefix
  - Whether the path prefix in traefik.path should be stripped when forwarding requests
    to the Service.
  - false
* - traefik.path
  - The path prefix to match when forwarding requests to the Service.
  - "/xxx"
```

## Installing the chart

To deploy a new service, cd to the `helm/charts` directory, then execute (define the varibles below or edit the script with your desired values):

```bash
helm upgrade -i ${MY_HELM_NAME} \
  ./charts/simple-service \
  -n myapp \
  --values values/${MY_VALUES_FILE}
```

It is recommended to name the helm release the same as your `app.name` value.

```{note}
To install the chart automatically at cluster creation, update the `init.sh` script.  For triggering upgrades when the associated Docker image is updated, update the `upgrade.sh` script.
```