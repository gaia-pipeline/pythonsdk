#!/bin/bash

# cleanup
rm -rf dist *.egg-info

# build dist
python setup.py sdist

# release
twine upload dist/*

