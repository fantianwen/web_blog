#!/usr/bin/env python3
# coding:utf-8

# common 工具集
import time


# 通过图片的路径，将该图片读成二进制数据
def save_image2char(image_path):
    with open(image_path, 'rb') as image:
        return image.read()


# 从时间戳获取年份
def get_year(t):
    return int(time.strftime('%Y', time.localtime(t)))


# 从时间戳获取月份
def get_month(t):
    return int(time.strftime('%m', time.localtime(t)))


# 从时间戳获取天
def get_day(t):
    return int(time.strftime('%d', time.localtime(t)))
