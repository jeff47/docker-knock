from xdg import xdg_config_home
import click, sys, shutil, subprocess, magic
from utils import run

def handle_acsm(acsm_path):
    drm_path = acsm_path.with_suffix('.drm')
    adobe_dir = xdg_config_home().joinpath('knock', 'acsm')
    adobe_dir.mkdir(parents=True, exist_ok=True)

    if drm_path.exists():
        click.echo(f"Error: {drm_path} must be moved out of the way or deleted.", err=True)
        sys.exit(1)

    if (
        not adobe_dir.joinpath('device.xml').exists()
        or not adobe_dir.joinpath('activation.xml').exists()
        or not adobe_dir.joinpath('devicesalt').exists()
    ):
        shutil.rmtree(str(adobe_dir))
        click.echo('This device is not registered with Adobe.')
        email = click.prompt("Enter your Adobe account's email address")
        password = click.prompt("Enter your Adobe account's password", hide_input=True)
        click.echo('Registering this device with Adobe...')

        run(
            [
                'adept_activate',
                '-u', email,
                '-O', str(adobe_dir)
            ],
            stdin=password+'\n',
            cleanser=lambda:shutil.rmtree(str(adobe_dir))
        )

    click.echo('Downloading the book from Adobe...')

    run([
        'acsmdownloader',
        '-d', str(adobe_dir.joinpath('device.xml')),
        '-a', str(adobe_dir.joinpath('activation.xml')),
        '-k', str(adobe_dir.joinpath('devicesalt')),
        '-o', str(drm_path),
        '-f', str(acsm_path)
    ])

    drm_path_type = magic.from_file(str(drm_path), mime=True)
    if drm_path_type == 'application/epub+zip':
        file_type = 'epub'
    elif drm_path_type == 'application/pdf':
        file_type = 'pdf'
    else:
        click.echo(f'Error: Received file of media type {drm_path_type} from Adobe\' servers.', err=True)
        click.echo('Only the following ACSM conversions are currently supported:', err=True)
        click.echo('  * ACSM -> EPUB', err=True)
        click.echo('  * ACSM -> PDF', err=True)
        click.echo('Please open a feature request at:', err=True)
        click.echo(f'  https://github.com/BentonEdmondson/knock/issues/new?title=Support%20{drm_path_type}%20Files&labels=enhancement', err=True)
        sys.exit(1)

    output_path = acsm_path.with_suffix('.' + file_type)
    if output_path.exists():
        drm_path.unlink()
        click.echo(f"Error: {output_path} must be moved out of the way or deleted.", err=True)
        sys.exit(1)

    click.echo('Decrypting the file...')

    run([
        'rmdrm-' + file_type,
        str(adobe_dir.joinpath('activation.xml')),
        str(drm_path),
        str(output_path)
    ])

    drm_path.unlink()

    click.secho(f'DRM-free {file_type.upper()} file created:\n{output_path}', fg='green')