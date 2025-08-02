# {{ cookiecutter.project_name }}

Initial repository for {{ cookiecutter.project_name }}.

## Configuration

Make sure `conf/smk_config.yml` has all the necessary parameters filled out.
Additionaly, `run.py` has a few hardcoded parameters, that need to be set specifically to your infrastructure.
These has been kept to a minimum, but required are still:

 - `WDIR`: The path to the actual working directory (where intermediate files will be stored).  
 - `SMK_PROFILE`: Name of (or path to) a working [snakemake profile](https://snakemake.readthedocs.io/en/stable/executing/cli.html#profiles).  
 - `RESULTSDIR`: Technically not needed (can be left as `./`). In case output files are defined (under RFS), these are kept in sync in this directory. Idea is to have a low-weight 'end result' directory. That can easily be shared.  


# CONFIG
CONFIGFILE = Path(__file__).parents[0] / 'conf' / 'smk_config.yml'
SMK_PROFILE = 'slurmsnake8'
WDIR = './'
RESULTSDIR = './'

## Usage

 > conda env create -f conf/env.yml  
 > conda activate {{ cookiecutter.project_name }}  
 > python run.py

