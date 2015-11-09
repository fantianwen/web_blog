#!/usr/bin/env python3
# coding:utf-8

# common 工具集
import io

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random


def save_image2char(image_path):
    with open(image_path, 'rb') as image:
        return image.read()


def rnd_color():
    rnd1 = random.randint(64, 255)
    rnd2 = random.randint(64, 255)
    rnd3 = random.randint(64, 255)
    return (rnd1, rnd2, rnd3)


def image2hex(image):
    output = io.BytesIO()
    image.save(output, format='JPEG')
    return output.getvalue()


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
