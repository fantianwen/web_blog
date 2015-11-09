#!/usr/bin/env python3
# coding:utf-8

import time
import os

from flask import Flask, request, render_template, session, flash, redirect, url_for
from jinja2 import Environment, FileSystemLoader

from utils import mylog, highlight
from models import Blog, next_id
import app_config


# 初始化flask的app
app = Flask(__name__)


@app.template_filter('datetime')
def datetime_filter(t):
    dt = time.strftime('%Y年 %m月 %d日', time.localtime(t))
    return dt


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

    init_jinja2(app.config, filters=dict(datetime=datetime_filter))
    # 运行server
    app.run(debug=mode)


@app.route('/<username>')
def index(username=None):
    if username is not None and username == 'fantianwen':
        session['admin'] = True
    else:
        session['admin'] = False
    return redirect(url_for('welcome'))


@app.route('/')
def welcome():
    session['page_number'] = 1
    blogs = Blog.find_all(orderBy='created_at desc', limit=(0, 5))
    return render_template('welcome.html', blogs=blogs)


@app.route('/page/<page_number>')
def show_page(page_number):
    int_page_number = int(page_number)
    session['page_number'] = int_page_number
    if page_number == 1:
        return redirect('/')
    blogs = Blog.find_all(orderBy='created_at desc', limit=((int_page_number - 1) * 5, 5))
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
