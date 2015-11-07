#!/usr/bin/env python3
# coding:utf-8

# 开发工程配置

from .default import Config


class DevelopmentConfig(Config):
    DEBUG = True

    '''
    web的访问地址
    '''

    WEB_URL = 'http://127.0.0.1:5000'

    SECRET_KEY = 'hahah'

    '''
    mysql的相关配置
    '''

    HOST = '127.0.0.1'

    PORT = 3306

    USER = 'root'

    PASSWORD = 'Fantianwen09'

    DB = 'awesome'
