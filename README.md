# Kubernetes test app

The following instructions assume a **Ubuntu 24.04LTS** host system.

## Preliminaries

For convenience, we have created a `git root` alias:
```bash
git config --global alias.root 'rev-parse --show-toplevel'
```
Ensure that you are in the project root before continuing below.

Ensure that `docker`, `kubectl`, `kind`, `helm`, and `screen` are installed. For `docker`, follow the [apt install instructions](https://docs.docker.com/engine/install/ubuntu/). For the other packages:
```bash
sudo snap install kubectl --classic
sudo snap install go --classic
sudo snap install helm --classic
go install sigs.k8s.io/kind@v0.23.0
sudo apt install screen
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

## Secrets

This repo contains a number of example secret files. Locate them using:
```bash
find . -path './mnt/*' -prune -o -name '*.example*' -print
```

Copy these files, removing ".example" from the filenames, and edit as desired.

## Running the cluster

All Kubernetes resources are associated with the `myapp` namespace.

### Initialisation

Use kind to start a cluster.  The file `kind.yaml` is used to set up our file mounts (e.g. for databases).
```bash
kind create cluster --config kind.yaml
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
myapp-frontend-main-77548d65d7-dmmkc   1/1     Running   0          11m
myapp-test-api-76b9486764-5rgp7        1/1     Running   0          12m
myapp-test-frontend-5b6b74f48d-whldq   1/1     Running   0          11m
postgres0-0                            1/1     Running   0          12m
traefik-5f9ddf59c-krgvf                1/1     Running   0          12m
```

### Tear-down
```bash
. destroy.sh
```

## Port forwarding (Kubernetes)

To expose a Kubernetes service, we can run `kubectl port-forward`. Utility functions for doing so are included in `load_scripts.sh`, i.e. `xxx_expose()`.  The `init.sh` script forwards the necessary ports automatically, using `screen` to provide persistence.

## Port forwarding (Docker)

For development, we may deploy containers on Docker without inserting them into the Kubernetes cluster. The Docker Compose file defines `host.docker.internal` so that Docker containers can communicate with the host machine and access any Kubernetes services that have been set up with `kubectl port-forward`.
