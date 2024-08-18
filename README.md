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
- myapp-api/README.md

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
kubectl get all,pv,pvc,secret -n myapp
```

*Example output:*
```
NAME                            READY   STATUS    RESTARTS   AGE
pod/myapp-api-8bbdcf645-fnb4b   1/1     Running   0          7m30s
pod/postgres-0                  1/1     Running   0          7m51s

NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/myapp-api     ClusterIP   10.96.58.175    <none>        3000/TCP   4m10s
service/postgres      ClusterIP   10.96.140.145   <none>        5432/TCP   7m51s
service/postgres-hl   ClusterIP   None            <none>        5432/TCP   7m51s

NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/myapp-api   1/1     1            1           7m30s

NAME                                  DESIRED   CURRENT   READY   AGE
replicaset.apps/myapp-api-8bbdcf645   1         1         1       7m30s

NAME                        READY   AGE
statefulset.apps/postgres   1/1     7m51s

NAME                           CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
persistentvolume/postgres-pv   10Gi       RWO            Retain           Bound    myapp/postgres-pvc                  <unset>                          7m54s

NAME                                 STATUS   VOLUME        CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/postgres-pvc   Bound    postgres-pv   10Gi       RWO                           <unset>                 7m54s

NAME                                    TYPE                 DATA   AGE
secret/postgres-passwords               Opaque               2      7m54s
secret/sh.helm.release.v1.postgres.v1   helm.sh/release.v1   1      7m51s
```

### Tear-down
```bash
. destroy.sh
```

## Port forwarding (Kubernetes)

To expose a Kubernetes service, we can run `kubectl port-forward`. Utility functions for doing so are included in `load_scripts.sh`, i.e. `xxx_expose()`.

## Port forwarding (Docker)

For development, we may deploy containers on Docker without inserting them into the Kubernetes cluster. The Docker Compose file defines `host.docker.internal` so that Docker containers can communicate with the host machine and access any Kubernetes services that have been set up with `kubectl port-forward`.

## Shell scripts

A set of shell scripts and functions are provided in `scripts/` and `load_scripts.sh`. A utility script `prepend_path` is required; copy this to a directory on your `$PATH`, e.g. `$HOME/.local/bin`.
