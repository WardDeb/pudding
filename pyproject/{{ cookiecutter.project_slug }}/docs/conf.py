from importlib.metadata import version as importlibversion

project = "{{ cookiecutter.project_name }}"
author = "WardDeb"
version = importlibversion("{{ cookiecutter.project_slug }}")
release = version

extensions = [
    'sphinx_click.ext'
]
language = "en"
master_doc = 'index'
pygments_style = 'sphinx'
source_suffix = '.rst'
html_theme = 'sphinx_rtd_theme'