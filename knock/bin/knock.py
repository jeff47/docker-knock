#!/usr/bin/env python3

import subprocess, shutil, click
from pathlib import Path
from getpass import getpass
from xdg import xdg_config_home

from handle_acsm import handle_acsm
from handle_aax import handle_aax

@click.command()
@click.argument(
    "path",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True
    )
)
def main(path):
    path = Path(path)

    # make the config dir if it doesn't exist
    xdg_config_home().joinpath('knock').mkdir(parents=True, exist_ok=True)

    path_type = path.suffix[1:].upper()

    if path_type == 'ACSM':
        click.echo('Received an ACSM (Adobe) file...')
        handle_acsm(path)
    #elif path_type == 'AAX':
    #    click.echo('Received an AAX (Audible) file...')
    #    handle_aax(path)
    else:
        click.echo(f'Error: Files of type {path_type} are not supported.\n', err=True)
        click.echo('Only the following file types are currently supported:', err=True)
        click.echo('  * ACSM (Adobe)\n', err=True)
        #click.echo('  * AAX (Audible)\n', err=True)
        click.echo('Please open a feature request at:', err=True)
        click.echo(f'  https://github.com/BentonEdmondson/knock/issues/new?title=Support%20{path_type}%20Files&labels=enhancement', err=True)
        sys.exit(1)

if __name__ == "__main__":
    main()