#!/usr/bin/env python
#coding=utf-8
import os
import time

import cyclone.web
from twisted.internet import reactor

from toughengine.radiusd.console import handlers
from toughengine.common import logger


###############################################################################
# web application
###############################################################################
class Application(cyclone.web.Application):
    def __init__(self, config=None, **kwargs):
        self.config = config

        try:
            if 'TZ' not in os.environ:
                os.environ["TZ"] = config.defaults.tz
            time.tzset()
        except:pass

        self.log = logger.Logger(config)

        settings = dict(
            cookie_secret=os.environ.get('cookie_secret', "12oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo="),
            static_path=os.path.join(os.path.dirname(__file__), "console/static"),
            debug=config.defaults.debug,
            config=self.config,
            xheaders=True,
        )

        all_handlers = [
            (r"/", handlers.HomeHandler),
            (r"/admin", handlers.AdminHandler),
        ]

        cyclone.web.Application.__init__(self, all_handlers,  **settings)



def run_admin(config):
    print "running radiusd admin"
    app = Application(config)
    reactor.listenTCP(int(config.admin.port), app, interface=config.admin.host)
    reactor.run()