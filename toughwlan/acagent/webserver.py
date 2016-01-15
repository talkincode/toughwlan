#!/usr/bin/env python
# coding:utf-8

import cyclone.web
from twisted.internet import reactor, defer
from urllib import urlencode
from toughlib import logger,utils
from toughlib import db_cache as cache
from toughlib.dbengine import get_engine

class LoginHandler(cyclone.web.RequestHandler):

    def get(self, *args, **kwargs):
        wlan_params = {
            "wlanuserip": utils.safestr(self.get_argument("wlanuserip", self.request.remote_ip)),
            "wlanusername": self.get_argument("username",""),
            "token" : self.get_argument("token",""),
            "wlanacip": self.settings.config.acagent.nasaddr,
            "ssid": self.get_argument("ssid","default"),
            "wlanusermac": self.get_argument("wlanusermac","00-00-00-00-00"),
            "wlanapmac": self.get_argument("wlanapmac","00-00-00-00-00"),
            "wlanuserfirsturl": self.get_argument("wlanuserfirsturl","/portal/index"),
            "callback": self.get_argument("callback","")
        }

        if all([wlan_params['wlanusername'],wlan_params['token']]):
            self.application.mcache.set("callback_token_%s" % wlan_params['wlanusername'],wlan_params['token'],300)
        elif all([wlan_params['wlanuserip'],wlan_params['token']]):
            self.application.mcache.set("callback_token_%s" % wlan_params['wlanuserip'],wlan_params['token'],300)
        elif all([wlan_params['wlanuserip'],wlan_params['callback']]):
            self.application.mcache.set("callback_cache_%s" % wlan_params['wlanuserip'],wlan_params['callback'],300)

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

    def __init__(self, config=None, dbengine=None, log=None, **kwargs):

        self.config = config
        self.log = log or logger.Logger(config)
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


def run(config, dbengine=None,log=None):
    app = AcWebAuth(config,dbengine, log=log)
    reactor.listenTCP(int(config.acagent.auth_port), app, interface=config.acagent.host)
