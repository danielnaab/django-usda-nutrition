#!/usr/bin/env python
import sys

from django.conf import settings
from django.core.management import execute_from_command_line


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'dev.db'
            }
        },
        INSTALLED_APPS=[
            'usda_nutrition',
            'tests',
        ],
        MIDDLEWARE_CLASSES=[],
    )


def runtests():
    #argv = sys.argv[:1] + ['makemigrations'] + sys.argv[1:]
    #execute_from_command_line(['makemigrations'])
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    runtests()
