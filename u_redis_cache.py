# -*- coding:utf-8 -*-
# @Author: wzy
# @Time: 2020-9-16 10:05:57
# 使用Redis数据库做缓存的相关工具函数
import logging
import pickle
# 依赖第三方包 redis
import redis
from typing import Any

_CacheClient_ = None


def init_cache(*args, **kwargs):
    global _CacheClient_
    _CacheClient_ = redis.StrictRedis(*args, **kwargs)


def set_cache(key: str, instance: Any, *args, **kwargs):
    assert _CacheClient_ is not None, "需要先执行init_cache方法"
    data = pickle.dumps(instance)
    try:
        _CacheClient_.set(key, data, *args, **kwargs)
    except Exception as e:
        logging.getLogger().error(e)
    finally:
        return instance


def get_cache(key: str, default: Any = None) -> Any:
    assert _CacheClient_ is not None, "需要先执行init_cache方法"
    try:
        data = _CacheClient_.get(key)
        if not data:
            return default
        default = pickle.loads(data)
    except Exception as e:
        logging.getLogger().error(e)
        return default
    else:
        return default


def del_cache(*keys: str):
    assert _CacheClient_ is not None, "需要先执行init_cache方法"
    try:
        _CacheClient_.delete(*keys)
    except Exception as e:
        logging.getLogger().error(e)
