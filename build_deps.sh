# Build Python dependencies and copy to local pypidev server
#
# The pypidev server should be set up to read package files from $HOME/pypackages.
# See: https://github.com/pypiserver/pypiserver?tab=readme-ov-file#using-the-docker-image

pushd `git root`/myapp-models
poetry build
rsync -avu dist/ $HOME/pypackages/myapp-models
popd
