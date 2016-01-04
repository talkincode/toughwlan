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

class PortalWebServer(cyclone.web.Application):

    def __init__(self, config=None, log=None, **kwargs):

        self.config = config

        self.syslog = log or logger.Logger(config)

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
        
        self.db_engine = get_engine(config)
        self.db = scoped_session(sessionmaker(bind=self.db_engine, autocommit=False, autoflush=False))
        self.session_manager = session.SessionManager(settings["cookie_secret"], self.db_engine, 600)
        self.mcache = cache.CacheManager(self.db_engine)

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
        load_handlers(handler_path=handler_path, pkg_prefix="toughwlan.portal",excludes=['views','webserver','portald'])

def run(config, log=log):
    app = PortalWebServer(config, log)
    reactor.listenTCP(int(config.portal.port), app, interface=config.portal.host)

