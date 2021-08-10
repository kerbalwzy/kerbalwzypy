# -*- coding:utf-8 -*-
# @Author: wzy
# @Time: 2021/8/10
# 字符处理工具函数


def contains_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False
