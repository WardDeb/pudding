from scripts.workflow_functions import calcHash, runSmk
from pathlib import Path
import sys
from rich import print

# CONFIG
CONFIGFILE = Path(__file__).parents[0] / 'smk_config.yml'
SMK_PROFILE = 'slurmsnake8'
WDIR = ''

# WORKFLOW
#runSmk(smk, CONFIGFILE, WDIR)
