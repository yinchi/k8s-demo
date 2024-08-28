# Kubernetes test app

The following instructions assume a **Ubuntu 24.04LTS** host system.

## Preliminaries

For convenience, we have created a `git root` alias:
```bash
git config --global alias.root 'rev-parse --show-toplevel'
```
Ensure that you are in the project root before continuing below.

Ensure that `docker`, `kubectl`, `kind`, and `helm` are installed. For `docker`, follow the [apt install instructions](https://docs.docker.com/engine/install/ubuntu/). For the other packages:
```bash
sudo snap install kubectl --classic
sudo snap install go --classic
sudo snap install helm --classic
go install sigs.k8s.io/kind@v0.23.0
```

A set of shell scripts and aliases are provided in `scripts/` and `load_scripts.sh`. A utility script `prepend_path` is required; copy this to a directory on your `$PATH`, e.g. `$HOME/.local/bin`.
```bash
cp copy_this_to_local_bin/prepend_path $HOME/.local/bin/prepend_path
```

Finally, enable and load our utility scripts:
```bash
chmod +x ./scripts/*.sh
. load_scripts.sh
```

We can read the documentation for each script using the `bashdoc` script, which displays the block comment at the top of the specified `.sh` file.

```bash
./scripts/bashdoc init.sh
```

## Setup

Create the files and directories as described in the "**Setup**" sections of:

- helm/postgres.md

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
kubectl get pod -n myapp
```

*Example output:*
```
NAME                                   READY   STATUS    RESTARTS   AGE
myapp-frontend-main-77548d65d7-gmr6r   1/1     Running   0          8m55s
myapp-test-api-64fc89c874-5bvgl        1/1     Running   0          9m6s
myapp-test-frontend-5b8cc77755-7t4vp   1/1     Running   0          8m55s
postgres-0                             1/1     Running   0          9m21s
traefik-5bff54c84c-7ckh6               1/1     Running   0          9m6s
```

### Tear-down
```bash
. destroy.sh
```

## Port forwarding (Kubernetes)

To expose a Kubernetes service, we can run `kubectl port-forward`. Utility functions for doing so are included in `load_scripts.sh`, i.e. `xxx_expose()`.

## Port forwarding (Docker)

For development, we may deploy containers on Docker without inserting them into the Kubernetes cluster. The Docker Compose file defines `host.docker.internal` so that Docker containers can communicate with the host machine and access any Kubernetes services that have been set up with `kubectl port-forward`.
