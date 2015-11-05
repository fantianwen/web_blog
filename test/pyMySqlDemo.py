#!/usr/bin/env python3
# coding:utf-8


import pymysql

connection = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='root',
                             password='Fantianwen09',
                             db='awesome',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        sql = "insert into Users (username,password) values (%s,%s);"
        cursor.execute(sql, ('hahha', '3333'))

    connection.commit()
finally:
    connection.close()
