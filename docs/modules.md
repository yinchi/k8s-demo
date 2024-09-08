# Modules

First-pary modules in this app are defined in `src/`.  Each module is a Python [Poetry](https://python-poetry.org/) project with a `Dockerfile`.  Docker images can be built using the `compose.yml` file; alternatively, the `init.sh` script will automatically build all images in `compose.yml`, push them to `ghcr.io`, and pull them into the Kubernetes node for launching the associated Pods.  Another option is to run `docker compose build --push` manually, then use `upgrade.sh` to upgrade the pods of a running cluster.

Note that, at the minimum, a module named `sample-module` requires a `sample_module/__init__.py` file and a `README.md` file.

## The `frontend-common` package

A `frontend-common` package (also implemented as a Poetry project) is included for providing templates for frontend design (using the [Plotly Dash](https://dash.plotly.com/) Python package and [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)).  This can be imported into other Poetry projects using `pyproject.toml`:

```toml
[tool.poetry.dependencies]
frontend-common = {path = "../frontend-common", develop = true}
```

Additionally, the `frontend-common` directory needs to be copied when building Docker images using this dependency; see `src/frontend-main/Dockerfile` for an example of this.

## The `frontend-main` package

The `frontend-main` package generates the root page of the webapp.  This contains a link to the frontends of each module as well as external links.  These links are defined in `src/frontend-common/frontend_common/module_meta.py`.

## Extra paths

In rare cases, you may need to manually edit the `extraPaths` configuration in `.vscode/settings.json`.  This will allow VSCode to find our Python files when running Intellisense.

## Module Testing with Docker Compose

The included `compose.yml` file allows us to start a set of services using `docker compose up`.  This can be useful for testing purposes. To connect to services in the Kubernetes node, use `kubectl port-forward` to expose the Kubernetes service to the host machine, and `host.docker.internal` to access the host machine from a Docker container.  The `test-api` service gives an example of this setup.

