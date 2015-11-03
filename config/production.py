#!/usr/bin/env python3
# coding:utf-8、


# 生产工程配置

from .default import Config


class ProductionConfig(Config):
    DEBUG = False
