# log

import click


class BaseLogger():

    def critical(msg):
        self.output(f"CRITICAL: {msg}")

    def error(msg):
        self.output(f"ERROR: {msg}")

    def warning(msg):
        self.output(f"WARNING: {msg}")

    def info(msg):
        self.output(msg)

    def debug(msg):
        self.output(f"# {msg}")


class RequestLogger(BaseLogger):

    def output(self, msg):
        yield msg


class OutputLogger(BaseLogger):

    def output(self, msg):
        click.echo(msg)
