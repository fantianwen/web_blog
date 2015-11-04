#!/usr/bin/env python3
# coding:utf-8

from utils import mylog
from flask import Flask, request, render_template, flash, url_for, redirect, session, stream_with_context,Response
from orm import Users

import asyncio

import orm

import app_config

from functools import update_wrapper


# 初始化flask的app
app = Flask(__name__)


#
# class StreamView(object):
#     """A decorator for flask view."""
#
#     def __init__(self, view_function):
#         self.view_function = view_function
#         update_wrapper(self, self.view_function)
#
#     def __call__(self, *args, **kwargs):
#         return_value = self.view_function(*args, **kwargs)
#         try:
#             response = iter(return_value)
#         except TypeError:
#             # the return value is not iterable
#             response = return_value
#             current_app.logger.warning(
#                 "The stream view %r isn't iterable." % self)
#         else:
#             # the return value is iterable
#             response = Response(return_value, direct_passthrough=True)
#         return response
#
#
# stream_view = StreamView

def stream_template(template_name, **context):
    # http://flask.pocoo.org/docs/patterns/streaming/#streaming-from-templates
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    # uncomment if you don't need immediate reaction
    ##rv.enable_buffering(5)
    return rv


@asyncio.coroutine
def create_app_and_init(loop):
    # 初始化配置
    mode = app_config.init_config(app)
    # 创建数据库连接池对象
    yield from orm.create_pool(loop)
    # 运行server
    app.run()


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    mylog.info('%s and %s' % (username, password))
    # save
    user = Users(username=username, password=password)
    mylog.info('%s' % user.__tableName__)
    # yield user.save()
    session['username'] = username
    user.save()
    return Response(stream_template('welcome.html'))


@app.route('/login')
def welcome():
    return render_template('welcome.html')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_app_and_init(loop))
    loop.run_forever()
