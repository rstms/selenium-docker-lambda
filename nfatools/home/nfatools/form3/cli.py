# cli

import click
import os
import pathlib

from .job import Job
from .server import app
from .db import Database
from configparser import ConfigParser

import logging
logger = logging.getLogger(__name__)

@click.group(name='form3')
@click.version_option()
@click.option('-v/-V', '--verbose/--no-verbose', default=False)
@click.option('-d', '--debug', is_flag=True, default=False)
@click.option('-c', '--config-file', default='/etc/nfatools/nfatools.conf', help='config file')
@click.option('-h', '--host', envvar='DB_HOST')
@click.option('-P', '--port', envvar='DB_PORT', default='3306')
@click.option('-u', '--user', envvar='DB_USER')
@click.option('-p', '--password', envvar='DB_PASSWORD')
@click.option('-d', '--database', envvar='DB_DATABASE')
@click.pass_context
def form3(ctx, verbose, debug, config_file, host, port, user, password, database):
    if debug:
        import pdb
        pdb.set_trace()
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['debug'] = debug
    ctx.obj['config_file'] = config_file
    if pathlib.Path(config_file).is_file():
        ctx.obj['config'] = ConfigParser().read(config_file)
    ctx.obj['db']=Database(host, port, user, password, database)

@form3.command()
@click.option('-i', '--index', default=1)
@click.pass_context
def run(ctx, index):
    """run a form3 job as a cli process"""
    job_data = ctx.obj['db'].get_job_data(index)
    return Job(job_data).run()

@form3.command()
@click.pass_context
def server(ctx):
    """run as an API server"""
    app.ctx = ctx
    return app.run()
