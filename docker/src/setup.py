from setuptools import setup, find_packages
from glob import glob
from os.path import basename, splitext
from pathlib import Path

here=Path(__file__).parent.resolve()

NAME='moonbat'
DESCRIPTION='remote selenium docker client example'
AUTHOR='Matt Krueger'
EMAIL='mkrueger@rstms.net'
URL='https://github.com/rstms/selenium-docker-lambda'

long_description = (here / 'README.md').read_text(encoding='utf-8')

__version__ = (here / NAME / 'VERSION').read_text(encoding='utf-8')

LICENSE = (here / NAME / 'LICENSE').read_text(encoding='utf-8')

install_requirements = [
  'arrow',
  'click',
  'flask',
  'selenium==4.0.0.a7',
  'mysql-connector',
  'bs4'
]
 
test_requirements = [
  'pytest',
  'pytest-click',
  'pytest-datadir'
]

setup(
    name=NAME,
    author=AUTHOR,
    author_email=EMAIL,
    version=__version__,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=('tests', 'docs', 'scripts')),
    package_data={NAME: ['VERSION', 'LICENSE']},
    install_requires=install_requirements,
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            f"{NAME}={NAME}.cli:cli"
        ],
    },
)
