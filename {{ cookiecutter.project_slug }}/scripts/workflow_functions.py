import hashlib
from rich import print
from pathlib import Path
import subprocess as sp


def calcHash(filepath):
    return hashlib.md5(
        open(filepath, 'rb').read()
    ).hexdigest()


def runSmk(smk, configfile, wdir, profile):
    print(f"[bold yellow] Running {Path(smk).stem} [/bold yellow]")
    opng = Path(wdir, 'DAGs' ,Path(smk).stem +'.png')
    opng.parents[0].mkdir(parents=True, exist_ok=True)
    rg = sp.Popen(
        [
            'snakemake',
            '-s', smk,
            '--configfile', configfile,
            '-d', wdir,
            '--filegraph',
            '--dryrun',
            '--quiet'
        ],
        stdout=sp.PIPE,
        stderr=sp.PIPE
    )
    rg.wait()
    print(f"plotting DAG under {opng}")
    with open(opng, 'w') as f:
        sp.Popen(
            ['dot', '-Tpng'],
            stdin=rg.stdout,
            stdout=f
        )
    f.close()
    print(f"Running ")
    ret = sp.run([
       'snakemake',
       '-s', smk,
       '--configfile', configfile,
       '--profile', profile,
       '-d', wdir
    ])
    return(ret.returncode)
