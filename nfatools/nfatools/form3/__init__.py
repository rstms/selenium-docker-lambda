# moonbat test client

from pathlib import Path

from .server import app

__version__ = (Path(__file__)/'VERSION').read_text().strip()
