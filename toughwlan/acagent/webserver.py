#!/usr/bin/env python
# coding:utf-8

import cyclone.web
from twisted.internet import reactor, defer
from urllib import urlencode
from toughlib import logger

class LoginHandler(cyclone.web.RequestHandler):

    def get(self, *args, **kwargs):
        wlan_params = {
            "wlanuserip": self.get_argument("userip", self.request.remote_ip),
            "wlanusername": self.get_argument("username","test"),
            "wlanacip": self.settings.config.acagent.nasaddr,
            "ssid": "default",
            "wlanusermac": self.get_argument("usermac","00:00:00:00:00"),
            "wlanapmac": "00:00:00:00:00",
            "wlanuserfirsturl": self.get_argument("firsturl","https://www.baidu.com")
        }
        url = "{0}?{1}".format(self.settings.config.acagent.portal_login, urlencode(wlan_params))
        print url
        self.redirect(url, permanent=False)

    @defer.inlineCallbacks
    def post(self):
        pass


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
        cyclone.web.Application.__init__(self, [(r"/", LoginHandler),],  **settings)


def run(config, dbengine=None,log=None):
    app = AcWebAuth(config,dbengine, log=log)
    reactor.listenTCP(int(config.acagent.auth_port), app, interface=config.acagent.host)
