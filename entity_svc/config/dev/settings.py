import os

from peewee import *

import utils

DEBUG=True
TEMPLATE_PATH = '%s/templates/' % os.path.dirname(os.path.realpath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'peewee.PostgresqlDatabase',
        'OPTIONS': {
            "database": os.environ.get('DB_NAME', "entitysvc_%s" % utils.get_env()),
            "user": os.environ.get('DB_USER', None),
            "password": os.environ.get('DB_PASS', None),
            "host": os.environ.get('DB_HOST', None),
        }
    }
}

MINIMUM_SCORE = 80
