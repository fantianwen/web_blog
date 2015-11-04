#!/usr/bin/env python3
# coding:utf-8

import asyncio
import aiomysql


@asyncio.coroutine
def get_pool(loop):
    # host = config.get('HOST')
    host = '127.0.0.1'
    print('host is : %s ' % host)

    # port = config.get('PORT')
    port = 3306
    # user = config.get('USER')
    user = 'root'
    # password = config.get('PASSWORD')
    password = 'Fantianwen09'
    # db = config.get('DB')
    db = 'awesome'
    # 获取数据库连接池的对象
    pool = yield from aiomysql.create_pool(host=host, port=port, user=user, password=password, db=db, loop=loop)
    return pool
