# -*- coding:utf-8 -*-
# @Author: wzy
# @Time: 2021/8/10
# SqlAlchemy ORM相关工具函数
from typing import Tuple

from sqlalchemy.orm import Query


# 查询集分页
def query_paginate(query: Query, page: int, limit: int) -> Tuple[list, int]:
    if limit:
        page_ob = query.paginate(page=page, per_page=limit, error_out=False)
        result = page_ob.items
        count = page_ob.total
    else:
        result = query.all()
        count = len(result)
    return result, count
