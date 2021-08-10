# -*- coding:utf-8 -*-
# @Author: wzy
# @Time: 2021-1-29 15:25:45
# 创建自定义的logger对象

import logging
from logging.handlers import RotatingFileHandler


class XLogger(logging.Logger):
    """
    自定义日志对象, 快速的实现文件输出, 以及捕获异常堆栈
    """
    DefaultOutputFmt = "%(asctime)s %(levelname)0.4s %(filename)s:%(lineno)d %(message)s"
    DefaultDateFmt = "%Y-%m-%d %H:%M:%S"

    def __init__(self, name=None, filepath=None, level=logging.DEBUG, fmt=DefaultOutputFmt,
                 date_fmt=DefaultDateFmt, max_bytes=1024 * 1024 * 10, backup_count=10):
        super().__init__(name)
        formatter = logging.Formatter(fmt=fmt, datefmt=date_fmt)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.addHandler(stream_handler)
        if filepath:
            file_handler = RotatingFileHandler(filename=filepath, maxBytes=max_bytes, backupCount=backup_count,
                                               encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.addHandler(file_handler)
        self.setLevel(level=level)

    def error(self, msg, *args, **kwargs):
        kwargs.setdefault('exc_info', True)
        super().error(msg, *args, **kwargs)
