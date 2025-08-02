import hashlib
from rich import print
from pathlib import Path
import subprocess as sp
import shutil
import datetime
import sys

def calcHash(filepath):
    return hashlib.md5(
        open(filepath, 'rb').read()
    ).hexdigest()

def shipResults(filetup, wdir, enddir, trackdic=None, delete=True):
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
        'created': 0,
        'deleted': 0
    }
    _checked_or_written = []

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
                    _checked_or_written.append(rfile)
                else:
                    tdic['unchanged'] += 1
                    _checked_or_written.append(rfile)
                continue
            else:
                shutil.copyfile(ofile, rfile)
                tdic['created'] += 1
                _checked_or_written.append(rfile)
    
    # There is no check to make sure that there are no duplicates in the incoming tuples.
    _checked_or_written = set(_checked_or_written)

    # Glob the enddir for files that are not in the _checked_or_written list, and delete them.
    if delete:
        for ofile in Path(enddir).glob('**/*'):
            if ofile.is_file() and ofile not in _checked_or_written and ofile.name != 'README.txt':
                ofile.unlink()
                tdic['deleted'] += 1
        for ofile in Path(enddir).glob('**/'):
            if ofile.is_dir() and not any(ofile.iterdir()):
                ofile.rmdir()

    # Book keeping.
    if trackdic:
        with open(Path(enddir) / 'README.txt', 'w') as f:
            _commit = sp.check_output(['git', 'log', '-n', '1', '--pretty=format:"%H"']).decode().strip('"')
            if not _commit:
                _commit = 'unknown'
            _remote = sp.check_output(['git', 'config', '--get', 'remote.origin.url']).decode().strip('"').strip('\n')
            if not _remote:
                _remote = 'unknown'

            _lw = 25
            f.write(f"{'Latest update on:':<{_lw}} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'Code created by:':<{_lw}} {trackdic['author']}\n")
            f.write(f"{'Results created with:':<{_lw}} {trackdic['repo']}\n")
            f.write(f"{'Repository code is at:':<{_lw}} {_commit}\n")
            f.write(f"{'Commit hash:':<{_lw}} {_remote}\n")

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
            '--rulegraph',
            '--dryrun',
            '--quiet'
        ],
        stdout=sp.PIPE,
        stderr=sp.PIPE
    )
    _stdout, _stderr = rg.communicate()
    # Some snakemake versions still print that 'building' line in stdout. Get rid of it.
    _stdout = _stdout.decode('utf-8').replace('Building DAG of jobs...\n', '').encode()

    if rg.returncode != 0:
        print(f"[bold red]Dryrun failed - return {rg.returncode}[/bold red]")
        for _line in _stdout.split('\n'):
            print(f"{_line}")
        sys.exit(rg.returncode)

    print(f"plotting DAG under {opng}")
    sp.run(
        ['dot', '-Tpng', '-o', opng],
        input=_stdout,
        check=True
    )
    print(f"Running ")
    ret = sp.run([
       'snakemake',
       '-s', smk,
       '--configfile', configfile,
       '--profile', profile,
       '-d', wdir
    ])
    return(ret.returncode)
