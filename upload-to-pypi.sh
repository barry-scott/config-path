#!/bin/bash
set -e
export TWINE_USERNAME=barryscott

tmp.venv/bin/python -m twine check dist/*
tmp.venv/bin/python -m twine upload --verbose -u __token__ -p $(<~/.config/pypi_token) dist/*
