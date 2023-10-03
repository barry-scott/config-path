#!/bin/bash
set -e
export TWINE_USERNAME=barryscott
PACKAGE=${1:?package to upload}
if [ ! -d "$PACKAGE" ]
then
    echo "Error: unknown package ${PACKAGE}"
    exit 1
fi

tmp.venv/bin/python -m twine check ${PACKAGE}/dist/*
tmp.venv/bin/python -m twine upload -u __token__ -p $(<.pypi_token) ${PACKAGE}/dist/*
