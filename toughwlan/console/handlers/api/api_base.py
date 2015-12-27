#!/usr/bin/env python
# coding:utf-8
import json
from hashlib import md5
from twisted.python import log
from toughlib import utils, apiutils
from toughwlan.console.handlers.base import BaseHandler
from toughlib.permit import permit
from toughwlan.console import models
import logging


class ApiHandler(BaseHandler):

    def check_xsrf_cookie(self):
        pass

    def parse_request(self):
        return apiutils.parse_request(self.settings.config.system.secret,self.request.body)
 




