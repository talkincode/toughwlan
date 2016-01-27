#!/usr/bin/env python
# coding:utf-8

import cyclone.web
from twisted.internet import reactor, defer
from urllib import urlencode
from toughlib import logger,utils,dispatch
from toughlib import db_cache as cache
from toughlib.dbengine import get_engine

class LoginHandler(cyclone.web.RequestHandler):

    def get(self, *args, **kwargs):
        wlan_params = {
            "wlanuserip": self.get_argument("userip", self.request.remote_ip),
            "ispcode": self.get_argument("ispcode", "default"),
            "wlanusername": self.get_argument("username","test"),
            "wlanacip": self.settings.config.acagent.nasaddr,
            "ssid": self.get_argument("ssid","default"),
            "wlanusermac": self.get_argument("wlanusermac","00-00-00-00-00"),
            "wlanapmac": self.get_argument("wlanapmac","00-00-00-00-00"),
            "wlanuserfirsturl": self.get_argument("wlanuserfirsturl","/portal/index"),
            "callback": self.get_argument("callback","")
        }
        dispatch.pub(EVENT_INFO, wlan_params)
        dispatch.pub(EVENT_INFO, "callback_cache_%s" % utils.safestr(wlan_params['wlanuserip']))
        self.application.mcache.set(
            "callback_cache_%s" % utils.safestr(wlan_params['wlanuserip']),wlan_params['callback'],300)

        url = self.settings.config.acagent.portal_login.format(**wlan_params)
        print url
        self.redirect(url, permanent=False)

    @defer.inlineCallbacks
    def post(self):
        pass

class NotifyHandler(cyclone.web.RequestHandler):
    def get(self, *args, **kwargs):
        print repr(self.request)
        self.write("notify ok!")


class AcWebAuth(cyclone.web.Application):

    def __init__(self, config=None, dbengine=None,**kwargs):

        self.config = config
        self.db_engine = dbengine or get_engine(self.config)
        self.mcache = cache.CacheManager(self.db_engine)
        settings = dict(
            cookie_secret="12oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/",
            xsrf_cookies=True,
            xheaders=True,
            config=self.config
        )
        cyclone.web.Application.__init__(self, [(r"/", LoginHandler),(r"/notify", NotifyHandler),],  **settings)


def run(config, dbengine=None):
    app = AcWebAuth(config,dbengine)
    reactor.listenTCP(int(config.acagent.auth_port), app, interface=config.acagent.host)
