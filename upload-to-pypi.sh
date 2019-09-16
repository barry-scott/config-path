#!/bin/bash
set -e
PY=python3.7
export TWINE_USERNAME=barryscott

${PY} -m twine check dist/*
${PY} -m twine upload dist/*
