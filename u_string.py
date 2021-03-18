# -*- coding:utf-8 -*-
# @Author: wzy
# @Time: 2021/3/18
# 字符串和字符相关的工具函数

__all__ = ['contains_chinese', 'hump_2_underline', 'underline_2_hump']


def contains_chinese(text):
    """
    检查整个字符串是否包含中文
    :param text: 需要检查的字符串
    :return: bool
    """
    for ch in text:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def hump_2_underline(text):
    """
    大小驼峰转换为下划线
    :param text: 需要转换的字符串
    :return:
    """
    res = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            res.append("_")
        res.append(char)
    return ''.join(res).lower()


def underline_2_hump(text, big=True):
    """
    下划线连接转为大小驼峰
    :param text: 需要转换的字符串
    :param big: 是否为大驼峰, 默认为True, 为False时表示要转换小驼峰
    """
    arr = text.lower().split('_')
    res = []
    for i in arr:
        res.append(i[0].upper() + i[1:])
    if not big:
        res[0] = res[0][0].lower() + res[0][1:]
    return ''.join(res)
