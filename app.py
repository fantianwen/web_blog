#!/usr/bin/env python3
# coding:utf-8

from utils import mylog
from flask import Flask, request, render_template, flash, url_for, redirect, session, stream_with_context, Response
from orm import Users

import asyncio

import app_config



# 初始化flask的app
app = Flask(__name__)


def create_app_and_init():
    # 初始化配置
    app_config.init_config(app)
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
    user.save()
    return render_template('welcome.html', username=username)


@app.route('/login')
def welcome():
    return render_template('welcome.html')


if __name__ == '__main__':
    create_app_and_init()
