#!/usr/bin/env python
#coding=utf-8

from hashlib import md5
from toughadmin.common import logger
from toughadmin.common.dbengine import get_engine
from sqlalchemy.orm import scoped_session, sessionmaker

class TaskProc:

    def __init__(self, config):
        self.config = config
        self.syslog = logger.Logger(config)
        self.db_engine = get_engine(config)
        self.db = scoped_session(sessionmaker(bind=self.db_engine, autocommit=False, autoflush=False))


    def mksign(self, secret, params=[]):
        _params = [str(p) for p in params if p is not None]
        _params.sort()
        _params.insert(0, secret)
        strs = ''.join(_params)
        return md5(strs.encode()).hexdigest().upper()