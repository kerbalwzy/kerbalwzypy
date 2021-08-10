# -*- coding:utf-8 -*-
# @Author: wzy
# @Time: 2021/3/18
# 时间处理相关函数
__all__ = ["UTC", "BJT", "PDT", "PST", "JST", "TimeZones", "XLanguageMonth2En", "time_cost_decorator",
           "utctime_form_iso8601", "utctime_form_x_format", "utc_today_zero", "utc_tomorrow_zero",
           "utc_2_bjt", "timestamp_2_bjt"]

import logging
import time
from functools import wraps
from datetime import timezone, timedelta, datetime, date
import dateutil.parser as date_parser
import dateutil.tz as tz

UTC = tz.UTC
BJT = tz.tzoffset("BJT", timedelta(hours=+8))  # 北京时间, CCTV4用这个缩写, 别BB
PDT = tz.tzoffset("PDT", timedelta(hours=-7))  # 太平洋夏令时
PST = tz.tzoffset("PST", timedelta(hours=-8))  # 太平洋标准时
JST = tz.tzoffset("JST", timedelta(hours=+9))  # 日本时间

TimeZones = {
    "UTC": UTC,
    "BJT": BJT,
    "PDT": PDT,
    "PST": PST,
    "JST": JST,
}

XLanguageMonth2En = {
    "enero": "Jan",
    "ene": "Jan",
    "january": "Jan",
    "jan": "Jan",
    "janv": "Jan",
    "januar": "Jan",
    "janvier": "Jan",
    "gennaio": "Jan",
    "gen": "Jan",
    "genn": "Jan",
    "januari": "Jan",
    "stycznia": "Jan",
    "stycz": "Jan",
    "sty": "Jan",
    "jän": "Jan",

    "febrero": "Feb",
    "febr": "Feb",
    "febbr": "Feb",
    "feb": "Feb",
    "fev": "Feb",
    "févr": "Feb",
    "fév": "Feb",
    "february": "Feb",
    "februar": "Feb",
    "février": "Feb",
    "febbraio": "Feb",
    "februari": "Feb",
    "luty": "Feb",
    "lut": "Feb",

    "marzo": "Mar",
    "mar": "Mar",
    "march": "Mar",
    "märz": "Mar",
    "mars": "Mar",
    "maart": "Mar",
    "maa": "Mar",
    "marzec": "Mar",

    "abril": "Apr",
    "abr": "Apr",
    "april": "Apr",
    "apr": "Apr",
    "avril": "Apr",
    "avr": "Apr",
    "aprile": "Apr",
    "kwietnia": "Apr",
    "kwiec": "Apr",
    "kwi": "Apr",

    "mayo": "May",
    "may": "May",
    "mai": "May",
    "maggio": "May",
    "mag": "May",
    "magg": "May",
    "mei": "May",
    "maj": "May",
    "maja": "May",

    "junio": "Jun",
    "jun": "Jun",
    "june": "Jun",
    "juni": "Jun",
    "juin": "Jun",
    "giugno": "Jun",
    "giu": "Jun",
    "czerwca": "Jun",
    "czerw": "Jun",
    "cze": "Jun",

    "julio": "Jul",
    "jul": "Jul",
    "july": "Jul",
    "juli": "Jul",
    "juil": "Jul",
    "juillet": "Jul",
    "luglio": "Jul",
    "lug": "Jul",
    "lugl": "Jul",
    "lipiec": "Jul",
    "lip": "Jul",

    "agosto": "Aug",
    "ago": "Aug",
    "ag": "Aug",
    "august": "Aug",
    "aug": "Aug",
    "août": "Aug",
    "aout": "Aug",
    "augustus": "Aug",
    "augusti": "Aug",
    "sierpnia": "Aug",
    "sierp": "Aug",
    "sie": "Aug",

    "septiembre": "Sep",
    "sep": "Sep",
    "september": "Sep",
    "sept": "Sep",
    "settembre": "Sep",
    "set": "Sep",
    "sett": "Sep",
    "wrzesień": "Sep",
    "wrzes": "Sep",
    "wrz": "Sep",

    "octubre": "Oct",
    "oct": "Oct",
    "october": "Oct",
    "oktober": "Oct",
    "okt": "Oct",
    "octobre": "Oct",
    "ottobre": "Oct",
    "ott": "Oct",
    "październik": "Oct",
    "pazdz": "Oct",
    "paz": "Oct",

    "noviembre": "Nov",
    "nov": "Nov",
    "november": "Nov",
    "novembre": "Nov",
    "listopad": "Nov",
    "listop": "Nov",
    "lis": "Nov",

    "diciembre": "Dec",
    "dic": "Dec",
    "december": "Dec",
    "dec": "Dec",
    "déc": "Dec",
    "dezember": "Dec",
    "décembre": "Dec",
    "dicembre": "Dec",
    "grudnia": "Dec",
    "grudz": "Dec",
    "gru": "Dec",
    "dez": "Dec",
}


def time_cost_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        s = time.time()
        res = func(*args, **kwargs)
        logging.getLogger().info("time-cost= {n} s".format(n=time.time() - s))
        return res

    return wrapper


def utctime_form_iso8601(value: str) -> datetime:
    temp_datetime = datetime.fromisoformat(value)
    utc_time = temp_datetime.astimezone(tz=timezone.utc)
    return utc_time


def utctime_form_x_format(x_format_datetime: str, special_format: str = None):
    """
    将常见的日期时间字符串转换为UTC时间对象, 要求字符串中必须携带时区信息;
    极少的特殊格式需要通过指定的special_format进行转换
    能处理的常见日期格式:
        Jun. 1, 2021 12:00:36 a.m. PDT
        Jun 22, 2021 12:08:32 AM PDT
        1 may. 2021 0:56:49 UTC
        1 mai 2021 00:02:22 UTC
        31 Mar 2021 23:07:47 UTC
        2021/05/01 13:20:34 JST
    不能处理的特殊格式:
        01.07.2021 22:01:45 UTC  (这样的字符串在日期和月份识别上存在错误情况, 必须通过指定格式处理)
    :param x_format_datetime: 带时区信息的日期时间字符串
    :param special_format: 特殊格式字符串
    """
    datetime_str, tz_str = x_format_datetime.rsplit(" ", 1)
    assert tz_str in TimeZones.keys(), RuntimeError("日期时间字符串携带的时区信息暂时无法处理, 需要补充常量值")
    if special_format:
        temp_datetime = datetime.strptime(datetime_str, special_format).replace(tzinfo=TimeZones[tz_str])
        return temp_datetime.astimezone(UTC)
    x_format_datetime = x_format_datetime.replace("a.m.", "AM").replace("p.m.", "PM").upper()
    for k, v in XLanguageMonth2En.items():
        k = k.upper()
        if k in x_format_datetime:
            x_format_datetime = x_format_datetime.replace(k, v)
            break
    temp_datetime = date_parser.parse(x_format_datetime, tzinfos=TimeZones)
    return temp_datetime.astimezone(UTC)


def utc_today_zero() -> date:
    return datetime.utcnow().date()


def utc_tomorrow_zero() -> date:
    return datetime.utcnow().date() + timedelta(days=1)


def utc_2_bjt(temp_time: datetime) -> datetime:
    return temp_time.replace(tzinfo=UTC).astimezone(tz=BJT)


def timestamp_2_bjt(temp_timestamp: int) -> datetime:
    return datetime.fromtimestamp(temp_timestamp).astimezone(tz=BJT)
