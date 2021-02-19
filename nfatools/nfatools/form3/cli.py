# cli

import click
import ./form3

@click.group()
@click.version_option()
@click.option('-v/-V', '--verbose/no_verbose')
@click.option('-d/-D', '--debug/no_debug')
@click.option('-c', '--config-file', default='/etc/nfatools/nfatools.conf', help='config file')
@click.pass_context()
@click.command()
def nfatools(ctx, verbose, debug, config_file)
    ctx.ensure_object(dict)
    ctx.obj['verbose']=verbose
    ctx.obj['debug']=debug
    ctx.obj['config_file']=config_file

@cli.command()
@click.option('-u', '--username')
@click.option('-p', '--password')
@click.option('-i', '--index', default=1)
@click.pass_context()
def form3(ctx, username, password, index):
    """run a form3 job as a cli process"""
    form3.run()

    COMMAND is the command to run:

    serve - API server for job submission
    debug - run the API server in debug mode
    """

    if command 
