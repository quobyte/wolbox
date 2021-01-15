#!/bin/bash

RUN_SCRIPT="$0"
RUN_DIR=$(dirname "${RUN_SCRIPT}")
VENV="${RUN_DIR}/venv"

if [ ! -d "${VENV}" ]; then
	python3 -m venv "${VENV}"
	source "${VENV}/bin/activate"
	python3 -m pip install -e .
else
	source "${VENV}/bin/activate"
fi

if [ ! "${1}" == "init" ]; then
    waitress-serve --call 'wolbox:create_app'
fi
