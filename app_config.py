#!/usr/bin/env python3
# coding:utf-8

import os
from utils import mylog

from config import load_config


def change_environ():
    os.environ['MODE'] = 'DEVELOPMENT'


def init_config(app):
    # 获取配置环境
    change_environ()
    # 获取配置文件，并进行flask的相关配置
    config = load_config()
    app.config.from_object(config)

    mylog.info('Debug mode is %s' % app.config['DEBUG'])

    return app.config['DEBUG']
