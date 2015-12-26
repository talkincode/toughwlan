#!/usr/bin/env python
#coding=utf-8
import time

from toughlib import utils
from toughlib.permit import permit
from toughwlan.console.handlers.api import api_base
from toughwlan.console import models


@permit.route(r"/api/admin")
class AdminhHandler(api_base.ApiHandler):

    def get(self):
        self.post()

    def post(self):
        self.render_json(msg="ok")


