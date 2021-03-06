#!/bin/bash
set -e
echo "Info: twine check ..."
python3 -m twine check dist/*
echo "Info: twine upload ..."
python3 -m twine upload dist/*
