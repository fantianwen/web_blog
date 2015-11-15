#!/usr/bin/env python3
# coding:utf-8

# 开发工程配置

from .default import Config


class DevelopmentConfig(Config):
    DEBUG = True

    '''
    web的访问地址
    '''

    WEB_URL = 'http://123.57.165.54'

    SECRET_KEY = 'hahah'

    '''
    mysql的相关配置
    '''

    HOST = '123.57.165.54'

    PORT = 3306

    USER = 'blog'

    PASSWORD = 'Fantianwen09'

    DB = 'blog'
