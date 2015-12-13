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
from toughportal.common import logger
from toughportal.console.portal import base, login
from txyam.client import YamClient

class Application(cyclone.web.Application):

    def __init__(self, config=None, **kwargs):

        self.config = config

        hosts = [h.split(":") for h in self.config.memcached.hosts.split(",")]
        hosts = [(h, int(p)) for h, p in hosts]
        self.mcache = YamClient(hosts)

        _handlers = [
            (r"/", base.HomeHandler),
            (r"/login", login.LoginHandler),
        ]

        try:
            if 'TZ' not in os.environ:
                os.environ["TZ"] = config.defaults.tz
            time.tzset()
        except:
            pass

        self.syslog = logger.Logger(config)

        settings = dict(
            cookie_secret="12oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/login",
            template_path=os.path.join(os.path.dirname(__file__), "views"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=self.config.defaults.debug,
            xheaders=True,
            config=self.config
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
                                        module_directory="/tmp/portal")

        cyclone.web.Application.__init__(self, _handlers, **settings)


    def run_normal(self):
        self.syslog.info('portal web server listen %s' % self.config.portal.host)
        reactor.listenTCP(int(self.config.portal.port), self, interface=self.config.portal.host)
        reactor.run()


def run(config):
    log.startLogging(sys.stdout)
    app = Application(config)
    app.run_normal()

