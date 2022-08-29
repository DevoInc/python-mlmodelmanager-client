#!/bin/bash
# Delete the dist folder
sudo rm -rf dist
# Build the new dist folder with the newest version
python3 -m build
