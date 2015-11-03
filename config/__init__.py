#!/usr/bin/env python3
# coding:utf-8


import os
import logging


def load_config():
    mode = os.environ.get('MODE')
    try:
        if mode == 'DEVELOPMENT':
            from .development import DevelopmentConfig
            return DevelopmentConfig
        elif mode == 'PRODUCTION':
            from .production import ProductionConfig
            return ProductionConfig
        else:
            from .testing import TestingConfig
            return TestingConfig
    except ImportError as e:
        logging.info('import Config file error', e)
        from .default import Config
        return Config
