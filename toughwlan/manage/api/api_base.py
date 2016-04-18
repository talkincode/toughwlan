#!/usr/bin/env python
# coding:utf-8
import json
from hashlib import md5
from toughlib import utils, apiutils, logger, storage
from toughwlan.manage.base import BaseHandler
from toughlib.permit import permit
from toughlib.apiutils import apistatus
from toughwlan import models


class ApiHandler(BaseHandler):

    def check_xsrf_cookie(self):
        pass

    def get_error_html(self, status_code=500, **kwargs):
        return self.render_result(code=apistatus.server_err.code, msg=u"%s:服务器处理失败" % status_code)

    def parse_request(self):
        return apiutils.parse_request(self.settings['config'].system.secret,self.request.body)

    def parse_form_request(self):
        return apiutils.parse_form_request(self.settings['config'].system.secret,self.get_params())

    def render_result(self, **result):
        resp = apiutils.make_message(self.settings['config'].system.secret, **result)
        if self.settings['debug']:
            logger.debug("[api debug] :: %s response body: %s" % (self.request.path, utils.safeunicode(resp)))
        self.write(resp)

    def _decode_msg(self,err, msg):
        _msg = msg and utils.safeunicode(msg) or apistatus.verify_err.msg
        if err and issubclass(type(a),BaseException):
            return u'{0}, {1}'.format(utils.safeunicode(_msg),utils.safeunicode(err.message))
        else:
            return _msg

    def render_success(self, msg=None, **result):
        self.render_result(code=apistatus.success.code,msg=self._decode_msg(None,msg),**result)

    def render_sign_err(self, err=None, msg=None):
        self.render_result(code=apistatus.sign_err.code,msg=self._decode_msg(err,msg))
 
    def render_parse_err(self, err=None, msg=None):
        self.render_result(code=apistatus.sign_err.code, msg=self._decode_msg(err,msg))
 
    def render_verify_err(self, err=None,msg=None):
        self.render_result(code=apistatus.verify_err.code, msg=self._decode_msg(err,msg))
 
    def render_server_err(self,err=None, msg=None):
        self.render_result(code=apistatus.server_err.code, msg=self._decode_msg(err,msg)) 

    def render_timeout(self,err=None, msg=None):
        self.render_result(code=apistatus.timeout.code, msg=self._decode_msg(err,msg)) 

    def render_limit_err(self,err=None, msg=None):
        self.render_result(code=apistatus.limit_err.code, msg=self._decode_msg(err,msg)) 

    def render_unknow(self,err=None, msg=None):
        self.render_result(code=apistatus.unknow.code, msg=self._decode_msg(err,msg))
 





