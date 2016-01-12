#!/usr/bin/env python
# coding:utf-8

import cyclone.web
from twisted.internet import reactor, defer
from urllib import urlencode
from toughlib import logger

class LoginHandler(cyclone.web.RequestHandler):

    def get(self, *args, **kwargs):
        wlan_params = {
            "wlanuserip": self.get_argument("wlanuserip", self.request.remote_ip),
            "wlanusername": self.get_argument("wlanusername",""),
            "wlanacip": self.settings.config.acagent.nasaddr,
            "ssid": self.get_argument("ssid","default"),
            "wlanusermac": self.get_argument("wlanusermac","00-00-00-00-00"),
            "wlanapmac": self.get_argument("wlanapmac","00-00-00-00-00"),
            "wlanuserfirsturl": self.get_argument("wlanuserfirsturl","/portal/index"),
            "callback": self.get_argument("callback","")
        }
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
