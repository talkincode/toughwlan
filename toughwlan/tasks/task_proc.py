#!/usr/bin/env python
#coding=utf-8

from hashlib import md5
from toughlib import logger
from toughlib.dbengine import get_engine
from sqlalchemy.orm import scoped_session, sessionmaker

class TaskProc:

    def __init__(self, config, log=None):
        self.config = config
        self.syslog = log or logger.Logger(config)
        self.db_engine = get_engine(config)
        self.db = scoped_session(sessionmaker(bind=self.db_engine, autocommit=False, autoflush=False))
