#!/usr/bin/env python3
# coding:utf-8

from flask import Flask

import os

from config import load_config

import logging

import asyncio

import database

logging.basicConfig(level=logging.INFO, format='van===>%(levelname)s : %(message)s')


def change_environ():
    os.environ['MODE'] = 'DEVELOPMENT'


@asyncio.coroutine
def create_app_and_init(loop):
    # 获取配置环境
    change_environ()

    # 初始化flask的app
    app = Flask(__name__)

    # 获取配置文件，并进行flask的相关配置
    config = load_config()
    app.config.from_object(config)

    logging.info('Debug mode is %s' % app.config['DEBUG'])

    # 初始化数据库连接池
    pool = yield from database.get_pool(loop, app.config)

    # 运行server
    app.run()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_app_and_init(loop))
    loop.run_forever()
