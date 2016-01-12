#!/usr/bin/env python
# coding:utf-8

import time
from toughlib import utils
from toughwlan.portal.base import BaseHandler
from twisted.internet import defer
from toughlib.permit import permit
from txportal import client
import functools

@permit.route(r"/portal/logout")
class LogoutHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/portal/login?ssid=default")
            return
        qstr = self.current_user.get("qstr","ssid=default")
        self.clear_session()
        self.redirect("/portal/login?%s"%qstr,permanent=False)