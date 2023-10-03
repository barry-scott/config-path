#!/bin/bash
d=$(pwd)
PY=${d}/tmp.venv/bin/python

${PY} -m colour_text "<>green Info:<> Installing wheels for ${PY}"
cd ${TMPDIR}
# cannot install from the source dir
${PY} -m pip install --upgrade --no-warn-script-location ${d}/*/dist/*.whl
