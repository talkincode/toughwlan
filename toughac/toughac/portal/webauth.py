#!/usr/bin/env python
# coding:utf-8

import cyclone.web
from twisted.internet import reactor
from urllib import urlencode
from toughac.common import logger

class LoginHandler(cyclone.web.RequestHandler):

    def get(self, *args, **kwargs):
        wlan_params = {
            "wlanuserip": self.request.remote_ip,
            "wlanusername": "testuser",
            "wlanacip": self.settings.config.ac.nasaddr,
            "ssid": "default",
            "wlanusermac": "00:00:00:00:00",
            "wlanapmac": "00:00:00:00:00",
            "wlanuserfirsturl": "https://www.baidu.com"
        }
        url = "{0}?{1}".format(self.settings.config.portal.login, urlencode(wlan_params))
        self.application.syslog.info(url)
        self.redirect(url, permanent=False)


class Application(cyclone.web.Application):

    def __init__(self, config=None, **kwargs):

        self.config = config
        self.syslog = logger.Logger(config)

        _handlers = [
            (r"/", LoginHandler),
        ]

        settings = dict(
            cookie_secret="12oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/",
            xsrf_cookies=True,
            xheaders=True,
            config=self.config
        )

        cyclone.web.Application.__init__(self, _handlers, **settings)


def run(config):
    print 'running acagent webauth {0}:{1}'.format(config.ac.host, config.ac.auth_port)
    web_factory = Application(config)
    reactor.listenTCP(int(config.ac.auth_port), web_factory, interface=config.ac.host)
    reactor.run()
