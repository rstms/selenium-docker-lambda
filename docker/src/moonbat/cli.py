# cli

import click
import nfatools_form3

@click.command()
@click.version_option()
@click.option('-u', '--username')
@click.option('-p', '--password')
@click.option('-i', '--index', default=1, help='db index')
def cli(username, password, index):
    return nfatools_form3.process_form(username, password)
