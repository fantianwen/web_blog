#!/usr/bin/env python3
# coding:utf-8

from utils import mylog
from flask import Flask, request, render_template, session
from jinja2 import Environment, FileSystemLoader

import time, os, datetime
from models import Blog
import app_config

# 初始化flask的app
app = Flask(__name__)


def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return '1分钟前'
    if delta < 3600:
        return '%s分钟前' % (delta // 60)
    if delta < 86400:
        return '%s小时前' % (delta // 3600)
    if delta < 604800:
        return '%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return '%s年%s月%s日' % (dt.year, dt.month, dt.day)


def init_jinja2(config, **kw):
    mylog.info('init jinja2...')
    options = dict(
        autoescape=kw.get('autoescape', True),
        block_start_string=kw.get('block_start_string', '{%'),
        block_end_string=kw.get('block_end_string', '%}'),
        variable_start_string=kw.get('variable_start_string', '{{'),
        variable_end_string=kw.get('variable_end_string', '}}'),
        auto_reload=kw.get('auto_reload', True)
    )
    path = kw.get('path', None)
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    mylog.info('set jinja2 template path: %s' % path)
    env = Environment(loader=FileSystemLoader(path), **options)
    filters = kw.get('filters', None)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    config['__templating__'] = env


def create_app_and_init():
    # 初始化配置
    mode = app_config.init_config(app)

    init_jinja2(app.config)
    # 运行server
    app.run(debug=mode)


@app.route('/<username>')
@app.route('/')
def index(username=None):
    if username is not None and username == 'fantianwen':
        session['admin'] = True
    else:
        session['admin'] = False

    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time() - 120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time() - 3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time() - 7200)
    ]
    return render_template('welcome.html', blogs=blogs)


@app.route('/login')
def login():
    return render_template('login.html')


def validate(username, password):
    if username == 'twfan_09@hotmail.com' and password == 'Fantianwen09':
        return True
    else:
        return False


@app.route('/write')
def write():
    return render_template('write.html')


if __name__ == '__main__':
    create_app_and_init()
