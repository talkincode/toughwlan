#!/usr/bin/env python
# coding:utf-8

import json
import cyclone.auth
import cyclone.escape
import cyclone.web
from hashlib import md5
from toughengine.radiusd import utils

class BaseHandler(cyclone.web.RequestHandler):
    
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)

    def check_xsrf_cookie(self):
        pass

    def initialize(self):
        self.log = self.application.log
        if self.settings.debug:
            self.log.info("[api debug] :::::::: %s request body: %s" % (self.request.path, self.request.body))
        
    def on_finish(self):
        pass


    def render_json(self, **template_vars):
        if not template_vars.has_key("code"):
            template_vars["code"] = 0
        resp = json.dumps(template_vars, ensure_ascii=False)
        if self.settings.debug:
            self.log.info("[api debug] :::::::: %s response body: %s" % (self.request.path, resp))
        self.write(resp)


    def make_sign(self, secret, params=[]):
        """ make sign
        :param params: params list
        :return: :rtype:
        """
        _params = [utils.safestr(p) for p in params if p is not None]
        _params.sort()
        _params.insert(0, secret)
        strs = utils.safestr(''.join(_params))
        # if self.settings.debug:
        #     self.log.info("sign_src = %s" % strs)
        mds = md5(strs).hexdigest()
        return mds.upper()

    def check_sign(self, secret, msg):
        """ check message sign
        :param msg: dict type  data
        :return: :rtype: boolean
        """
        if "sign" not in msg:
            return False
        sign = msg['sign']
        params = [msg[k] for k in msg if k != 'sign']
        local_sign = self.make_sign(secret, params)
        # if self.settings.debug:
        #     self.log.info("[api debug] :::::::: remote_sign = %s ,local_sign = %s" % (sign, local_sign))
        return sign == local_sign

    def parse_request(self):
        try:
            msg_src = self.request.body
            req_msg = json.loads(msg_src)
        except Exception as err:
            self.log.error('parse params error %s' % utils.safestr(err))
            raise ValueError("parse params error")

        if not self.check_sign(self.settings.config.radiusd.key, req_msg):
            raise ValueError("message sign error")

        return req_msg