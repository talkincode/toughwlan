#!/usr/bin/env python
# coding:utf-8

import time
from toughlib import utils
from toughwlan.portal.base import BaseHandler
from twisted.internet import defer
from toughlib.permit import permit
from txportal import client
import functools

@permit.route(r"/portal/index")
class HomeHandler(BaseHandler):
    def get(self):
        tpl_name = self.get_argument("tpl_name",'default')
        self.render(self.get_index_template(tpl_name))

