#!/usr/bin/env python
# coding: utf-8

import pytest
from basedir import basedir
import os
import shutil
import sys

import logging

# Create Logger
logger = logging.getLogger('app')


def main():
    argv = []

    argv.extend(sys.argv[1:])

    pytest.main(argv)

    try:
        os.remove(os.path.join(basedir, '.coverage'))

    except OSError:
        pass

    try:
        shutil.rmtree(os.path.join(basedir, '.cache'))

    except OSError:
        pass

    try:
        shutil.rmtree(os.path.join(basedir, 'test/.cache'))
    except OSError:
        pass


if __name__ == '__main__':
    main()
