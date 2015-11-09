#!/usr/bin/env python3
# coding:utf-8

# common 工具集


def save_image2char(image_path):
    with open(image_path, 'rb') as image:
        return image.read()

