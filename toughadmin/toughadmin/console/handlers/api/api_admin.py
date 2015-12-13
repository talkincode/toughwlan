#!/usr/bin/env python
#coding=utf-8
import time

from toughadmin.common import utils
from toughadmin.common.permit import permit
from toughadmin.console.handlers.api import api_base
from toughadmin.console import models


@permit.route(r"/api/admin")
class AdminhHandler(api_base.ApiHandler):

    def get(self):
        self.post()

    def post(self):
        self.render_json(msg="ok")


