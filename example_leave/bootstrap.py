#!/usr/bin/env python

import os
import sys

# setup the environment
SETTINGS = 'example_leave.settings'
os.environ['DJANGO_SETTINGS_MODULE'] = SETTINGS


def cmd(txt):
    os.system(txt)


def actions(cmds):
    for c in cmds:
        cmd(c)


def start():
    actions([
        'rm db.sqlite3',
        'sleep 1',
        './manage.py migrate --noinput',
        './manage.py createsuperuser --email=admin@me.org',
    ])


def run_sample_data():
    cmd('python sample_data.py')


def main():
    start()
    run_sample_data()


if __name__ == '__main__':
    main()
