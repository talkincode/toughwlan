#!/usr/bin/env python
# coding:utf-8
import json
from hashlib import md5
from toughlib import utils, apiutils, logger
from toughwlan.admin.base import BaseHandler
from toughlib.permit import permit
from toughwlan import models

class ApiHandler(BaseHandler):

    def check_xsrf_cookie(self):
        pass

    def get_error_html(self, status_code=500, **kwargs):
        return self.render_result(code=1, msg=u"%s:服务器处理失败" % status_code)

    def parse_request(self):
        return apiutils.parse_request(self.settings.config.system.secret,self.request.body)

    def parse_form_request(self):
        return apiutils.parse_form_request(self.settings.config.system.secret,self.get_params())

    def render_result(self, **result):
        resp = apiutils.make_message(self.settings.config.system.secret, **result)
        if self.settings.debug:
            logger.debug("[api debug] :: %s response body: %s" % (self.request.path, utils.safeunicode(resp)))
        self.write(resp)
 




