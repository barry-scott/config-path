#!/bin/bash
echo "Info: cleaning tmp and build files"
rm -rf tmp.venv
rm -f  *.log

find . -name 'dist' -exec rm -rf {} +
find . -name '*.egg-info' -exec rm -rf {} +
find . -name '.mypy_cache' -exec rm -rf {} +
