# -*- coding:utf-8 -*-
# @Author: wzy
# @Time: 2020-8-6 16:34:10
# 生成UPC编码, 随机生成的UPC编码不一定就是可用的, 说不定已经被其他人注册使用过了
from random import randint

__all__ = ["generate_upc_code", "upc_check_num"]


def upc_check_num(code: str):
    """
    获取校验位数字
    :param code: UPC编码前11位
    """
    check_digit = int(code[0]) + int(code[2]) + int(code[4]) + int(code[6]) + int(code[8]) + int(code[10])
    check_digit = 3 * check_digit
    check_digit = int(code[1]) + int(code[3]) + int(code[5]) + int(code[7]) + int(code[9]) + check_digit
    if check_digit % 10 == 0:
        return str(0)
    else:
        return str(10 - (check_digit % 10))


def upc_eleven_num(prefix: str = ""):
    """
    随机生成upc前n位数字
    """
    if prefix and not prefix.isdigit():
        raise Exception("前缀错误, 必须是数字")
    if len(prefix) > 10:
        raise Exception("前缀错误, 长度要不能超过10个数字")
    _code = prefix
    for _ in range(11 - len(_code)):
        _i = randint(0, 9)
        _code += str(_i)
    return _code


def generate_upc_code(prefix: str = ""):
    _code = upc_eleven_num(prefix=prefix)
    return _code + upc_check_num(_code)
