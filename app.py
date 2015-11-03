#!/usr/bin/env python3
# coding:utf-8

from flask import Flask

import os

from config import load_config

import logging

logging.basicConfig(level=logging.INFO, format='van===>%(levelname)s : %(message)s')


def change_environ():
    os.environ['MODE'] = 'DEVELOPMENT'


def create_app():
    change_environ()

    app = Flask(__name__)

    config = load_config()
    app.config.from_object(config)

    logging.info('Debug mode is %s' % app.config['DEBUG'])


if __name__ == '__main__':
    create_app()
