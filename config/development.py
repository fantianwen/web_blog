#!/usr/bin/env python3
# coding:utf-8

# 开发工程配置

from .default import Config


class DevelopmentConfig(Config):

    DEBUG = True

    WEB_URL = 'http://127.0.0.1:5000'


