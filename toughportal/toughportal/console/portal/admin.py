#!/usr/bin/env python
# coding:utf-8

from toughportal.console.portal.base import BaseHandler


class PortalError(Exception):pass

class AdminHandler(BaseHandler):

    def get(self):
        self.post()

    def post(self):
        self.render_json(msg="ok")

