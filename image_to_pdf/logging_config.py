# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import logging
from logging.config import dictConfig

logging_config = dict(
    version=1,
    formatters={
        'f': {'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
              'datefmt': '%Y-%m-%d %H:%M:%S'
              }
        },
    handlers={
        'file': {'class': 'logging.handlers.RotatingFileHandler',
                 'formatter': 'f',
                 "filename": "error.log",
                 "maxBytes": 1024 * 1024 * 200,
                 "backupCount": 3,
                 'level': logging.WARNING},
        'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'f',
                    'level': logging.INFO,
                    'stream': 'ext://sys.stdout'}

        },
    root={
        'handlers': ['file', 'console'],
        'level': logging.INFO,
        },
)


def setup_logging_config():
    dictConfig(logging_config)
