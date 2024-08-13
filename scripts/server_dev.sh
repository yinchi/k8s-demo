#!/usr/bin/env bash
#
# Run the `myapp` server on bare metal (no containerisaton).

pushd `git root`/myapp/myapp
poetry run fastapi dev main.py
popd