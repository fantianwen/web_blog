#!/usr/bin/env python3
# coding:utf-8

import asyncio
import aiomysql


@asyncio.coroutine
def get_pool(loop, config):
    host = config.get('HOST')

    print('host is : %s ' % host)

    port = config.get('PORT')
    user = config.get('USER')
    password = config.get('PASSWORD')
    db = config.get('DB')
    # 获取数据库连接池的对象
    pool = yield from aiomysql.create_pool(host=host, port=port, user=user, password=password, db=db, loop=loop)
    return pool
