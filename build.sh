#!/bin/bash
rm -rf  build
rm -rf  dist
rm -rf  config-path.egg-info

python3 setup.py sdist bdist_wheel "$@"
python3 -m twine check dist/*

ls -1 dist/*.whl
