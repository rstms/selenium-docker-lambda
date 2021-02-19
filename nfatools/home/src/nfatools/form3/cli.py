# cli

import click
from .job import Job
from .server import app
from .log import OutputLogger


@click.group()
@click.version_option()
@click.option('-v/-V', '--verbose/no_verbose')
@click.option('-d/-D', '--debug/no_debug')
@click.option('-c', '--config-file', default='/etc/nfatools/nfatools.conf', help='config file')
@click.pass_context()
@click.command()
def form3(ctx, verbose, debug, config_file):
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['debug'] = debug
    ctx.obj['config_file'] = config_file


@cli.command()
@click.option('-h', '--host')
@click.option('-u', '--username')
@click.option('-p', '--password')
@click.option('-d', '--database')
@click.option('-i', '--index', default=1)
@click.pass_context()
def run(ctx, host, username, password, database, index):
    """run a form3 job as a cli process"""
    return Job(db(host, username, password, database, index, OutputLogger()))


@cli.command()
@click.pass_context()
def server(ctx):
    """run as an API server"""
    app.run()
    return
