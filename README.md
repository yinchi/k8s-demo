# Kubernetes test app

The following instructions assume a **Ubuntu 24.04LTS** host system.

## Preliminaries

For convenience, we have created a `git root` alias:
```bash
git config --global alias.root 'rev-parse --show-toplevel'
```

Ensure that `docker`, `kubectl`, `kind`, and `helm` are installed. For `docker`, follow the [apt install instructions](https://docs.docker.com/engine/install/ubuntu/). For the other packages:
```bash
sudo snap install kubectl --classic
sudo snap install go --classic
sudo snap install helm --classic
go install sigs.k8s.io/kind@v0.23.0
```

Finally, enable our utility scripts:
```bash
cd `git root`
chmod +x ./scripts/*.sh
```

We can read the documentation for each script using the `bashdoc.sh` script, which displays the block comment at the top of the specified `.sh` file.

```bash
./scripts/bashdoc.sh ./scripts/bashdoc.sh
```

## Setup

Create the files and directories as described in the "**Setup**" sections of:

- postgres/README.md

## Running the cluster

All Kubernetes resources are associated with the `myapp` namespace.

### Initialisation

Use kind to start a cluster.  The file `config.yaml` is used to set up our file mounts (e.g. for databases).
```bash
kind create cluster --config config.yaml
```

Next, initialise all our resources (secrets, services, persistent volumes etc.):
```bash
. init.sh
```

Ensure that everything is running:
```bash
kubectl get svc,pod,pv,pvc,secret -n myapp
```

*Example output:*
```
NAME                  TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
service/postgres      ClusterIP   10.96.99.218   <none>        5432/TCP   82m
service/postgres-hl   ClusterIP   None           <none>        5432/TCP   82m

NAME             READY   STATUS    RESTARTS   AGE
pod/postgres-0   1/1     Running   0          82m

NAME                           CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
persistentvolume/postgres-pv   10Gi       RWO            Retain           Bound    myapp/postgres-pvc                  <unset>                          82m

NAME                                 STATUS   VOLUME        CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/postgres-pvc   Bound    postgres-pv   10Gi       RWO                           <unset>                 82m

NAME                                    TYPE                 DATA   AGE
secret/postgres-passwords               Opaque               2      82m
secret/sh.helm.release.v1.postgres.v1   helm.sh/release.v1   1      82m
```

### Tear-down
```bash
. destroy.sh
```

## Set up a local Docker registry

For development purposes, we want to make our images available to Kubernetes without pushing every single build to a public registry. Instead, we can create a local registry for our images:
```bash
pushd `git root`
./scripts/local_registry_init.sh
popd
```

Test the new registry as follows:
```bash
docker pull hello-world:latest
docker image tag hello-world:latest localhost:5000/hello-world:latest
docker push localhost:5000/hello-world:latest
docker run --rm -it --pull=always localhost:5000/hello-world:latest
```

Return a list of available images and tags:
```bash
./scripts/local_registry_list.sh
```

To remove the registry and its associated Docker volume:
```bash
docker stop registry && docker rm -v registry
```

## Shell scripts

A set of shell scripts are provided in `scripts/` for interacting with the local Docker registry and the webserver container.
