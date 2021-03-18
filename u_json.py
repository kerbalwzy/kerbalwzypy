# -*- coding:utf-8 -*-
# @Author: wzy
# @Time: 2021/3/18
# JSON字符串或可被JSON序列化的对象的常用工具函数

import json
import re
from typing import Union

from u_string import hump_2_underline, underline_2_hump

__all__ = ['json_str_key_hump_2_underline', 'json_str_key_underline_2_hump', 'json_obj_key_underline_2_hump',
           'json_obj_key_hump_2_underline']


def __re_hump_2_underline(match_obj):
    text = match_obj.group(1)
    text = text[0] + hump_2_underline(text=text[1:-2]) + text[-2:]
    return text


def json_str_key_hump_2_underline(json_str: str):
    """
    将JSON字符中的key由大小驼峰转换为下划线连接
    """
    instance = re.compile(r'("\w+":)')
    json_str = instance.sub(repl=__re_hump_2_underline, string=json_str)
    return json_str


def json_obj_key_hump_2_underline(json_obj: Union[dict, list]):
    """
    将JSON对象中的key由大小驼峰转换为下划线连接
    """
    return json.loads(json_str_key_hump_2_underline(json.dumps(json_obj)))


def __re_underline_2_big_hump(match_obj):
    text = match_obj.group(1)
    text = text[0] + underline_2_hump(text=text[1:-2], big=True) + text[-2:]
    return text


def __re_underline_2_small_hump(match_obj):
    text = match_obj.group(1)
    text = text[0] + underline_2_hump(text=text[1:-2], big=False) + text[-2:]
    return text


def json_str_key_underline_2_hump(json_str: str, big: bool = True):
    """
    将JSON字符串中的key由下划线转换为大小驼峰, 默认为大驼峰
    """
    instance = re.compile(r'("\w+":)')
    if big:
        json_str = instance.sub(repl=__re_underline_2_big_hump, string=json_str)
    else:
        json_str = instance.sub(repl=__re_underline_2_small_hump, string=json_str)
    return json_str


def json_obj_key_underline_2_hump(json_obj: Union[dict, list], big: bool = True):
    """
    将JSON对象中的key由下划线转换为大小驼峰, 默认为大驼峰
    """
    return json.loads(json_str_key_underline_2_hump(json.dumps(json_obj), big=big))
