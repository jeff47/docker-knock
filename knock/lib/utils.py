import click, subprocess, sys

# run a command and display output in a styled terminal
# cleanser is called if the command returns a >0 exit code
def run(command: [str], stdin: str = '', cleanser = lambda: None) -> int:

    open_fake_terminal(' '.join(command))

    result = subprocess.run(
        command,
        stderr=subprocess.STDOUT,
        input=stdin.encode(),
        check=False # don't throw Python error if returncode isn't 0
    )

    close_fake_terminal(result.returncode, cleanser)

    return result.returncode


def open_fake_terminal(command: str):
    click.secho('', fg='white', bg='black', bold=True, reset=False)

    # show command
    click.echo(f'knock> {command}')

    # remove bold
    click.secho('', fg='white', bg='black', bold=False, reset=False)


def close_fake_terminal(exit_code: int, cleanser = lambda: None):
    click.secho(f'\nknock[{exit_code}]>', bold=True)

    # newline
    click.echo('')

    if exit_code > 0:
        cleanser()
        click.echo(f'Error: Command returned error code {exit_code}.', err=True)
        sys.exit(1)

def verify_absence_of(file_path):
    if m4b_path.exists():
        click.echo(f"Error: {file_path} must be moved out of the way or deleted.", err=True)
        sys.exit(1)