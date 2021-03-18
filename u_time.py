# -*- coding:utf-8 -*-
# @Author: wzy
# @Time: 2021/3/18
# 时间处理相关函数
import logging
import time
from functools import wraps
from datetime import timezone, timedelta, datetime

CST = timezone(timedelta(hours=8))
UTC = timezone.utc


def utc_today_zero():
    return datetime.utcnow().date()


def utc_tomorrow_zero():
    return datetime.utcnow().date() + timedelta(days=1)


def utc_2_cst(temp_time: datetime):
    return temp_time.replace(tzinfo=UTC).astimezone(tz=CST)


def timestamp_2_cst(temp_timestamp: int):
    return datetime.fromtimestamp(temp_timestamp).astimezone(tz=CST)


def time_cost(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        s = time.time()
        res = func(*args, **kwargs)
        logging.getLogger().info("time-cost= {n} s".format(n=time.time() - s))
        return res

    return wrapper
