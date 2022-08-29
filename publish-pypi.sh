#!/bin/bash
# Delete the dist folder
sudo rm -rf dist
# Build the new dist folder with the newest version
python3 -m build
# Get variables from .env
export $(xargs < .env)
# Publish the result to TestPypi
twine upload dist/* -u ${PYPI_USERNAME} -p ${PYPI_PASSWORD}
