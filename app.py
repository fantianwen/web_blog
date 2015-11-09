#!/usr/bin/env python3
# coding:utf-8

import time
import os

from flask import Flask, request, render_template, session, flash, redirect, url_for, Response
from jinja2 import Environment, FileSystemLoader

from utils import mylog, highlight, common
from models import Blog, Comment, User, next_id
import app_config


# 初始化flask的app
app = Flask(__name__)


@app.template_filter('datetime')
def datetime_filter(t):
    formatted_time = time.strftime('%Y年 %m月 %d日', time.localtime(t))
    return formatted_time


@app.template_filter('detail_time')
def detail_time_filter(t):
    formatted_time = time.strftime('%Y年%m月%d日 %H:%M:%S', time.localtime(t))
    return formatted_time


def get_avator_or_404(user_name):
    # users = User.find_all('name= ?', [user_name])
    # print('长度是。。。。。。。', len(users))
    guest_image_path = 'static/img/user.png'
    image = common.save_image2char(guest_image_path)
    return image


@app.route('/avatar/<user_name>.png')
def avatar(user_name):
    mylog.info('user_name is %s' % user_name)
    user_image = get_avator_or_404(user_name=user_name)
    return Response(user_image, mimetype='image/png')


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
    blogs = Blog.find_all(orderBy='created_at desc', limit=(0, 8))
    return render_template('welcome.html', blogs=blogs)


@app.route('/page/<page_number>')
def show_page(page_number):
    int_page_number = int(page_number)
    session['page_number'] = int_page_number
    if page_number == 1:
        return redirect('/')
    blogs = Blog.find_all(orderBy='created_at desc', limit=((int_page_number - 1) * 8, 8))
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
    # TODO 添加自己的头像
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


@app.route('/blog/<id>', methods=['GET', 'POST'])
def blog_id(id):
    guest_image_path = 'static/img/user.png'
    if request.method == 'POST':
        comment_content = request.form['comment_content']
        comment_name = request.form['comment_name']
        comment = Comment(id=next_id(), blog_id=id, user_id='guest', user_name=comment_name,
                          user_image='',
                          content=comment_content, created_at=time.time())
        comment.save()
        user = User(id=next_id(), email='', passwd='', admin=0, name=comment_name,
                    image=common.save_image2char(guest_image_path),
                    created_at=time.time())
        # TODO 先使用name来进行判定是否唯一，后期希望能够使用email来判断是否唯一
        _user = User.find_all('name= ?', [comment_name])
        if len(_user) == 0:
            user.save()
        flash('comment and new user had been saved successfully!')

    blog = Blog.find(id)
    md_text = highlight.parse2markdown(blog.content)
    blog.html_content = md_text
    comments = Comment.find_all('blog_id= ?', [id])
    return render_template('blogdetail.html', blog=blog, comments=comments)


if __name__ == '__main__':
    create_app_and_init()
