from scripts.workflow_functions import runSmk, shipResults
from pathlib import Path
import sys
from rich import print

# CONFIG
CONFIGFILE = Path(__file__).parents[0] / 'conf' / 'smk_config.yml'
SMK_PROFILE = 'slurmsnake8'
WDIR = './'
RESULTSDIR = './'

# TRACKDIC
trackdic = {
    'author': "{{ cookiecutter.full_name }}",
    'repo': "{{ cookiecutter.project_slug }}",
}

# RUN WORKFLOW
#runSmk(smk, CONFIGFILE, WDIR, SMK_PROFILE)

# SHIP RESULTS
RFS = [
    ('results/*',)
]

# Update results
print(shipResults(RFS, WDIR, RESULTSDIR, trackdic))