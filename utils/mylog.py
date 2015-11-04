#!/usr/bin/env python3
# coding:utf-8

import logging

logging.basicConfig(level=logging.INFO, format='van===>%(levelname)s : %(message)s')


def info(msg):
    logging.info(msg)
