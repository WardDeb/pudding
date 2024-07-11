import hashlib
from rich import print
from pathlib import Path
import subprocess as sp
import shutil


def calcHash(filepath):
    return hashlib.md5(
        open(filepath, 'rb').read()
    ).hexdigest()


def shipResults(filetup, wdir, enddir):
    '''
    filetup is a tuple consisting of:
    (filepath, folder, fint)

    where filepath is the relative path (relative to wdir) to a results file.
    folder (optional) is a folder where the file will be placed in (relative to enddir).
    fint (optional) is an integer that renames the sourcefile to a combination of the fint's upstream folders.

    for example:
        filetup = ('RNA/res.txt') -> enddir/res.txt
        filetup = ('RNA/res.txt', 'expr') -> enddir/expr/res.txt
        filetupe = ('RNA/res.txt', 'expr', 1) -> enddir/expr/RNA_res.txt
        filetupe = ('exprs/RNA/res.txt', 'expr', 2) -> enddir/expr/exprs_RNA_res.txt
    
    Note that filepath can be a pattern: 'RNA/*.txt' will take all txt files.
    '''

    tdic = {
        'replaced': 0,
        'unchanged': 0,
        'created': 0
    }
    for _ftup in filetup:
        for ofile in Path(wdir).glob(_ftup[0]):
            if len(_ftup) == 1:
                rfile = Path(enddir) / ofile.name
            elif len(_ftup) == 2:
                rfile = Path(enddir) / Path(_ftup[1]) / ofile.name
            else:
                assert len(_ftup) == 3
                assert isinstance(_ftup[2], int)
                newn = '_'.join(ofile.parts[:-1][-_ftup[2]:]) + '_' + ofile.name
                rfile = Path(enddir) / Path(_ftup[1]) / newn
            rfile.parents[0].mkdir(parents=True, exist_ok=True)
            # Only copy when file doesn't exist, or hash is different.
            if rfile.is_file():
                if calcHash(ofile) != calcHash(rfile):
                    shutil.copy(ofile, rfile)
                    tdic['replaced'] += 1
                else:
                    tdic['unchanged'] += 1
                continue
            else:
                shutil.copyfile(ofile, rfile)
                tdic['created'] += 1
    return tdic


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
