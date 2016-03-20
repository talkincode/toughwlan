#!/usr/bin/env python
#coding:utf-8
import sys
import os
import time
import cyclone.web
from twisted.python import log
from twisted.internet import reactor
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from mako.lookup import TemplateLookup
from sqlalchemy.orm import scoped_session, sessionmaker
from toughlib import utils
from toughlib import logger
from toughwlan import models
from toughwlan.manage.settings import redis_conf
from toughlib.dbengine import get_engine
from toughlib.permit import permit, load_handlers
from toughlib import redis_cache
from toughlib import redis_session
from toughlib.db_backup import DBBackup
import toughwlan



class Httpd(cyclone.web.Application):
    def __init__(self, config=None, dbengine=None, **kwargs):

        self.config = config

        settings = dict(
            cookie_secret="12oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/login",
            template_path=os.path.join(os.path.dirname(toughwlan.__file__), "views"),
            static_path=os.path.join(os.path.dirname(toughwlan.__file__), "static"),
            xsrf_cookies=True,
            config=self.config,
            debug=self.config.system.debug,
            xheaders=True,
        )

        self.cache = CacheManager(**parse_cache_config_options({
            'cache.type': 'file',
            'cache.data_dir': '/tmp/cache/data',
            'cache.lock_dir': '/tmp/cache/lock'
        }))

        self.tp_lookup = TemplateLookup(directories=[settings['template_path']],
                                        default_filters=['decode.utf8'],
                                        input_encoding='utf-8',
                                        output_encoding='utf-8',
                                        encoding_errors='replace',
                                        module_directory="/tmp/toughwlan")

        self.db_engine = dbengine
        self.db = scoped_session(sessionmaker(bind=self.db_engine, autocommit=False, autoflush=False))

        redisconf = redis_conf(config)
        self.session_manager = redis_session.SessionManager(redisconf,settings["cookie_secret"], 600)
        self.mcache = redis_cache.CacheManager(redisconf,cache_name='ToughWlanWeb-%s'%os.getpid())
        self.mcache.print_hit_stat(10)

        self.db_backup = DBBackup(models.get_metadata(self.db_engine), excludes=[
            'trw_online','system_session','system_cache'])

        self.aes = utils.AESCipher(key=self.config.system.secret)

        permit.add_route(cyclone.web.StaticFileHandler,
                         r"/backup/download/(.*)",
                         u"下载数据",
                         u"系统管理",
                         handle_params={"path": self.config.database.backup_path},
                         order=1.0405)

        handler_path = os.path.join(os.path.abspath(os.path.dirname(toughwlan.__file__)), "manage")
        load_handlers(handler_path=handler_path, pkg_prefix="toughwlan.manage",excludes=['views','httpd','ddns_task'])

        cyclone.web.Application.__init__(self, permit.all_handlers, **settings)



def run(config, dbengine=None):
    app = Httpd(config, dbengine=dbengine)
    reactor.listenTCP(config.admin.port, app, interface=config.admin.host)

