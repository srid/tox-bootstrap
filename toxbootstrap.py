#!/usr/bin/env python

import sys
import os
from os import path
from urllib import urlretrieve
import logging
from subprocess import check_call, CalledProcessError

logging.basicConfig(level=logging.INFO)


VIRTUALENVPY_URL = 'http://bitbucket.org/ianb/virtualenv/raw/tip/virtualenv.py'


def run(cmd, shell=True):
    """Run the given command in shell"""
    logging.info('Running command: %s', cmd)
    check_call(cmd, shell=shell)
    

def wget(url):
    """Download the given file to current directory"""
    logging.info('Downloading %s', url)
    localpath = path.join(path.abspath(os.getcwd()), path.basename(url))
    urlretrieve(url, localpath)
    

def has_script(venv, name):
    """Check if $name ($name.exe) is found in the virtualenv scripts directory"""
    if sys.platform == 'win32':
        return any([path.exists(path.join(venv, 'Scripts', name)),
                    path.exists(path.join(venv, 'Scripts', name + '.exe'))])
    else:
        return path.exists(path.join(venv, 'bin', name))


def get_script_path(venv, name):
    """Return the full path the script in virtualenv directory"""
    if sys.platform == 'win32':
        p = path.join(venv, 'Scripts', name)
        if not path.exists(p):
            p = path.join(venv, 'Scripts', name + '.exe')
    else:
        p = path.join(venv, 'bin', name)

    if not path.exists(p):
        raise NameError('cannot find a script named "{0}"'.format(name))

    return p


def main():
    os.chdir(path.abspath(path.dirname(__file__)))
    if not path.isdir('.tox'):
        os.mkdir('.tox')
    os.chdir('.tox')

    # create virtual environment
    if not path.isdir('toxinstall'):
        # get virtualenv.py
        if not path.isfile('virtualenv.py'):
            wget(VIRTUALENVPY_URL)
        assert path.isfile('virtualenv.py')

        # XXX: we use --no-site-packages because: if tox is installed in global
        # site-packages, then pip will not install it locally. ideal fix for
        # this should be to first look for tox in the global scripts/ directory.
        run('python virtualenv.py --no-site-packages --distribute toxinstall')

    assert has_script('toxinstall', 'python')
    assert has_script('toxinstall', 'pip')

    # install/upgrade tox itself
    if not has_script('toxinstall', 'tox'):
        run('{0} install --upgrade --download-cache=pip-cache tox'.format(
                get_script_path('toxinstall', 'pip')))

    assert has_script('toxinstall', 'tox')
    tox_script = path.abspath(get_script_path('toxinstall', 'tox'))
    logging.info('tox is already installed at %s', tox_script)

    # Now run the locally-installed tox
    try:
        run([tox_script] + sys.argv[1:], shell=False)
    except CalledProcessError as e:
        logging.error('tox exited with error code %d', e.returncode)


if __name__ == '__main__':
    main()
