#!/bin/bash
# Delete the dist folder
sudo rm -rf dist
# Build the new dist folder with the newest version
python3 -m build
# Get variables from .env
export $(xargs < .env)
# Publish the result to TestPypi
twine upload --repository testpypi dist/* -u ${TESTPYPI_USERNAME} -p ${TESTPYPI_PASSWORD}
