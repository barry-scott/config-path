#!/bin/bash
PY=python3.7
rm -rf  build
rm -rf  dist
rm -rf  config-path.egg-info

${PY} setup.py sdist bdist_wheel "$@"
${PY} -m twine check dist/*

ls -1 dist/*.whl
