#!/usr/bin/env python3
# coding:utf-8

# common 工具集
import io
import time
import random

from PIL import Image, ImageDraw, ImageFont


# 通过图片的路径，将该图片读成二进制数据
def save_image2char(image_path):
    with open(image_path, 'rb') as image:
        return image.read()


# 随机获取一个颜色（RGB的表示）
def rnd_color():
    rnd1 = random.randint(64, 255)
    rnd2 = random.randint(64, 255)
    rnd3 = random.randint(64, 255)
    return (rnd1, rnd2, rnd3)


# 将一个Image类型的图片对象转化成十六进制数据
def image2hex(image):
    output = io.BytesIO()
    image.save(output, format='JPEG')
    return output.getvalue()


# 通过用户的名字的首字母生成其头像（avatar）
def create_avatar_by_name(name):
    width = 10
    height = 10
    cf = name[0]
    image = Image.new('RGB', (width, height), (255, 255, 255))
    font = ImageFont.truetype('Arial.ttf', 36)
    draw = ImageDraw.Draw(image)
    rc = rnd_color()
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rc)
    draw.text((12, 12), cf, font=font, fill=rnd_color())
    return image2hex(image)


# 从时间戳获取年份
def get_year(t):
    return int(time.strftime('%Y', time.localtime(t)))


# 从时间戳获取月份
def get_month(t):
    return int(time.strftime('%m', time.localtime(t)))


# 从时间戳获取天
def get_day(t):
    return int(time.strftime('%d', time.localtime(t)))
