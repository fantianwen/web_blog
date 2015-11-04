#!/usr/bin/env python3
# coding:utf-8

import asyncio
import aiomysql


@asyncio.coroutine
def get_pool():
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
    pool = yield from aiomysql.create_pool(host=host, port=port, user=user, password=password, db=db)
    return pool


@asyncio.coroutine
def haha():
    pool = yield from get_pool()
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        yield from cur.execute("select * from student;")
        re = yield from cur.fetchall()
        print(re)
    pool.close()
    yield from pool.wait_closed()


asyncio.get_event_loop().run_until_complete(haha())



