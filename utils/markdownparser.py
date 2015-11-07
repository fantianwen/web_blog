#!/usr/bin/env python3
# coding:utf-8




def parse2markdown(text):
    renderer = HighlightMixin()
    markdown = mistune.Markdown(renderer=renderer)
    return markdown(text)
