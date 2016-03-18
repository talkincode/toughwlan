#!/usr/bin/env python
#coding:utf-8
import sys
import time
import os
import cyclone.web
from twisted.python import log
from twisted.internet import reactor
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from mako.lookup import TemplateLookup
from toughlib import logger
from toughlib.permit import permit, load_handlers
from sqlalchemy.orm import scoped_session, sessionmaker
from toughlib.dbengine import get_engine
from toughlib import db_session as session
from toughlib import db_cache as cache
import toughwlan

class Httpd(cyclone.web.Application):

    def __init__(self, config=None, dbengine=None, **kwargs):

        self.config = config

        settings = dict(
            cookie_secret="12oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/login",
            template_path=os.path.join(os.path.dirname(__file__), "views"),
            static_path=os.path.join(os.path.dirname(toughwlan.__file__), "static"),
            xsrf_cookies=True,
            debug=self.config.system.debug,
            xheaders=True,
            config=self.config
        )
        
        self.db_engine = dbengine
        self.db = scoped_session(sessionmaker(bind=self.db_engine, autocommit=False, autoflush=False))
        self.session_manager = session.SessionManager(settings["cookie_secret"], self.db_engine, 600)
        self.mcache = cache.CacheManager(self.db_engine,cache_name="ToughWlanPortal")

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
                                        module_directory="/tmp/portal")
        self.init_route()
        cyclone.web.Application.__init__(self, permit.all_handlers, **settings)

    def init_route(self):
        handler_path = os.path.join(os.path.abspath(os.path.dirname(toughwlan.__file__)), "portal")
        load_handlers(handler_path=handler_path, pkg_prefix="toughwlan.portal",excludes=['views','httpd','portald'])

def run(config, dbengine=None):
    app = Httpd(config, dbengine)
    reactor.listenTCP(int(config.portal.port), app, interface=config.portal.host)

