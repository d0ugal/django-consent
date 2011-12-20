#!/usr/bin/env python

import os
import sys


def runtests(*test_args):

    parent = os.path.dirname(os.path.abspath(__file__))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'consent.tests.settings'
    sys.path.insert(0, parent)

    from django.core.management import ManagementUtility

    utility = ManagementUtility()
    command = utility.fetch_command('test')
    command.execute(verbosity=1)
    sys.exit()


if __name__ == '__main__':
    runtests()
