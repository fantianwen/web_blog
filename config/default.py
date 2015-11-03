#!/usr/bin/env python3
# coding:utf-8

# 默认的工程配置


class Config(object):
    # 默认是debug模式
    DEBUG = True

    # 默认发布出去的url地址
    WEB_URL = 'http://127.0.0.1:5000'

    # database 参数设置
    HOST = '127.0.0.1'
    PORT = 3306
    USER = 'radasm'
