#!/usr/bin/env python
# coding=utf-8
import datetime
import os
import six
import msgpack
import toughwlan
from txzmq import ZmqEndpoint, ZmqFactory, ZmqPushConnection, ZmqPullConnection
from twisted.internet import protocol
from twisted.internet import reactor
from twisted.internet import defer
from toughlib import utils
from toughlib import logger
from toughlib import db_cache as cache
from toughlib.dbengine import get_engine
from txradius.radius import dictionary
from txradius import message
from toughlib.utils import timecast
from toughlib.storage import Storage
from toughwlan.radiusd.settings import *
from toughwlan import models
import decimal
decimal.getcontext().prec = 16
decimal.getcontext().rounding = decimal.ROUND_UP


class RADIUSWorker(object):

    def __init__(self, config, dbengine):
        self.config = config
        self.dict = dictionary.Dictionary(os.path.join(os.path.dirname(toughwlan.__file__), 'dictionarys/dictionary'))
        self.db_engine = dbengine or get_engine(config)
        self.aes = utils.AESCipher(key=self.config.system.secret)
        self.cache = cache.CacheManager(self.db_engine)

    @property
    def master_radius(self):
        def fetch_result():
            table = models.TrwRadius.__table__
            with self.db_engine.begin() as conn:
                return conn.execute(table.select().where(table.c.serv_type==1)).first()
        return self.cache.aget(master_radius_cache_key,fetch_result, expire=3600)

    def find_nas(self,ip_addr):
        def fetch_result():
            table = models.TrwBas.__table__
            with self.db_engine.begin() as conn:
                return conn.execute(table.select().where(table.c.ip_addr==ip_addr)).first()
        return self.cache.aget(bas_cache_key(ip_addr),fetch_result, expire=3600)

    def find_account(self,account_number):
        def fetch_result():
            table = models.TrwAccount.__table__
            with self.db_engine.begin() as conn:
                return conn.execute(table.select().where(table.c.account_number==account_number)).first()
        return self.cache.aget(account_cache_key(account_number),fetch_result, expire=3600*24*30)

    def find_account_attrs(self,account_number):
        def fetch_result():
            table = models.TrwAccountAttr.__table__
            with self.db_engine.begin() as conn:
                return conn.execute(table.select().where(table.c.account_number==account_number)).all()
        return self.cache.aget(account_attrs_cache_key(account_number),fetch_result, expire=3600*24*30)

    def add_online(self,online):
        table = models.TrwOnline.__table__
        with self.db_engine.begin() as conn:
            conn.execute(table.insert().values(**online)) 

    def is_online(self, nasaddr, session_id):
        table = models.TrwOnline.__table__
        with self.db_engine.begin() as conn:
            return conn.execute(table.count().where(
                table.c.nas_addr==nasaddr).where(
                table.c.session_id==session_id)).scalar() > 0

    def get_online(self, nasaddr, session_id):
        table = models.TrwOnline.__table__
        with self.db_engine.begin() as conn:
            return conn.execute(table.select().where(
                table.c.nas_addr==nasaddr).where(
                table.c.session_id==session_id)).first()       

    def del_online(self, nasaddr, session_id):
        table = models.TrwOnline.__table__
        with self.db_engine.begin() as conn:
            stmt = table.delete().where(
                table.c.nas_addr==nasaddr).where(
                table.c.session_id==session_id)
            conn.execute(stmt)

    def get_input_total(self,ticket):
        bl = decimal.Decimal(ticket['acct_input_octets'])/decimal.Decimal(1024)
        gl = decimal.Decimal(ticket['acct_input_gigawords'])*decimal.Decimal(4*1024*1024)
        tl = bl + gl
        return int(tl.to_integral_value())   
        
    def get_output_total(self,ticket):
        bl = decimal.Decimal(ticket['acct_input_octets'])/decimal.Decimal(1024)
        gl = decimal.Decimal(ticket['acct_output_gigawords'])*decimal.Decimal(4*1024*1024)
        tl = bl + gl
        return int(tl.to_integral_value())      




