# Quickstart

We will assume a Ubuntu 24.04LTS host system and `bash` shell throughout this documentation.

## Build and runtime dependencies

Install `docker`, `kubectl`, `kind`, `helm`, and `screen`.  For Docker, follow the instructions for [installing Docker using `apt`](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository).  For the other software packages:

```bash
sudo snap install kubectl --classic
sudo snap install helm --classic
sudo snap install go --classic
go install sigs.k8s.io/kind@latest
sudo apt install screen
```

```console
$ which docker kubectl kind helm screen
/usr/bin/docker
/snap/bin/kubectl
/home/yinchi/go/bin/kind
/snap/bin/helm
/usr/bin/screen
```

## Development dependences

For development, we recommend Visual Studio Code (**VSCode**). Poetry is used for Python package management, install this as follows:

```bash
sudo apt install pipx
pipx install poetry

# Optional plugins
poetry self add poetry-dockerize-plugin
poetry self add poetry-plugin-export

# Show plugins
poetry self show plugins
```

Next, `cd` into each subdirectory of `src/` and run `poetry install`.

You will probably also want to install the following **VSCode** extensions:

- [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)
- [pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint)
- [Go Template Support](https://marketplace.visualstudio.com/items?itemName=jinliming2.vscode-go-template)
- [Helm Intellisense](https://marketplace.visualstudio.com/items?itemName=Tim-Koehler.helm-intellisense)
- [Kubernetes](https://marketplace.visualstudio.com/items?itemName=ms-kubernetes-tools.vscode-kubernetes-tools)
- [Poetry Monorepo](https://marketplace.visualstudio.com/items?itemName=ameenahsanma.poetry-monorepo)

## Bash scripts

Copy the files in `copy_this_to_local_bin` to a directory on your `$PATH`, e.g. `$HOME/.local/bin`. Currently, this is just `prepend_path`, which is used to add our `scripts` directory to the `$PATH` environment variable.

## Launching the Kubernetes stack

The file `kind.yaml` defines the configuration for our `kind` cluster, including extra mounts for database persistence.

Start the `kind` cluster with:
```bash
kind create cluster --config kind.yaml
```

Finally, source the `init.sh` script:
```bash
. init.sh
```

This script will:
- Build all containers in the Docker Compose file (`compose.yml`)
- Create an `myapp` namespace in Kubernetes
- Create all the `myapp` resources (services, secrets, persistent volumes, etc.)
- Forward ports for the frontend (8000) and Traefik dashboard (9000), using `screen`.

The stack can be torn down using `. destroy.sh`. To remove the cluster entirely, use `kind delete cluster`.

## Bash aliases

The `load_scripts.sh` file contains a number of `bash` aliases and functions for convenience. For example, we can use `ns myapp` to make `myapp` the default namespace, or `pods` to list the currently running pods in the `myapp` namespace (in the current `kind` context).

The `init.sh` file calls `load_scripts.sh` automatically. Alternatively, we can execute `. load_scripts.sh` manually.