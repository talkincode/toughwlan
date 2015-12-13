#!/usr/bin/env python
# coding:utf-8

from toughengine.radiusd.console.base import BaseHandler
from toughengine.radiusd import utils


class HomeHandler(BaseHandler):

    def get(self):
        self.post()

    def post(self):
        self.render_json(code=0,msg="ok")



class AdminHandler(BaseHandler):

    def get(self):
        self.post()

    def post(self):
        self.render_json(code=0, msg="ok")

