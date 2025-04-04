#!/bin/bash
## Bash script, to create a new virtual environment, install all requirements and run main commands.
## GNU/Linux only at the moment. Should use Scripts instead of bin on Windows.

# exit on errors
set -eux

unset PYTHONPATH PYTHONSTARTUP
MYENV="./venv_spacewalks.$(date +%Y%m%d_%H%M%S)"
python3 -m venv "${MYENV}"
source "./${MYENV}/bin/activate"
python3 -m pip install -r requirements.txt
python3 eva_data_analysis.py
python3 eva_data_analysis.py ./data/eva-data.json out.csv
python3 -m pytest --cov --cov-report=html
mkdocs build
mkdocs gh-deploy
howfairis https://github.com/mtav/spacewalks
echo SUCCESS
