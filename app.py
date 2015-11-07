#!/usr/bin/env python3
# coding:utf-8

from utils import mylog, highlight
from flask import Flask, request, render_template, session, flash
from jinja2 import Environment, FileSystemLoader

import time, os, datetime
from models import Blog, User, Comment, next_id
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
    blogs = Blog.find_all(orderBy='created_at desc')
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


@app.route('/save_blog', methods=['POST'])
def save_blog():
    id = next_id()
    user_id = 'admin'
    user_name = 'fantianwen'
    user_image = ''
    name = request.form['blog_title']
    summary = request.form['blog_summary']
    content = request.form['blog_content']
    created_at = time.time()

    blog = Blog(id=id, user_id=user_id, user_name=user_name, user_image=user_image, name=name, summary=summary,
                content=content, created_at=created_at)
    blog.save()
    flash('保存成功')
    return render_template('/welcome.html')


@app.route('/blog/<id>', methods=['GET'])
def blog_id(id):
    blog = Blog.find(id)
    md_text = highlight.parse2markdown(blog.content)
    blog.html_content = md_text
    return render_template('blogdetail.html', blog=blog)


if __name__ == '__main__':
    create_app_and_init()
