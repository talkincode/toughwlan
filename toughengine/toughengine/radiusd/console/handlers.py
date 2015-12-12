#!/usr/bin/env python
# coding:utf-8

from toughengine.radiusd.console.base import BaseHandler
from toughengine.radiusd.console import tester
from toughengine.radiusd import utils

AuthHandler = tester.AuthHandler
AcctHandler = tester.AcctHandler

class HomeHandler(BaseHandler):

    def get(self):
        self.post()

    def post(self):
        self.render_json(code=0,msg="ok")


NAS_CACHE_UPDATE_NOTIFY = 'nas_update'
NOTIFYS = (NAS_CACHE_UPDATE_NOTIFY,)

class NotifyHandler(BaseHandler):

    def get(self):
        self.post()

    def post(self):
        self.render_json(code=0, msg="ok")


class NasAllHandler(BaseHandler):
    test_nas = {
        'code':0,
        'msg':'ok',
        'ipaddr':"127.0.0.1",
        'secret':"123456",
        'vendor_id':"0",
        'coa_port':3799,
        'api_secret':"rpWE9AtfDPQ3ufXBS6gJ37WW8TnSF930",
        'api_auth_url':"http://127.0.0.1:1815/test/authorize",
        'api_acct_url':"http://127.0.0.1:1815/test/acctounting",
        'nonce':"1231414214234",
    }

    def get(self):
        self.post()

    def post(self):
        try:
            req_msg = self.parse_request()
        except Exception as err:
            self.render_json(msg=utils.safestr(err.message))
            return

        _data = self.test_nas.copy()
        _sign = self.make_sign(self.settings.api_secret,_data.values())
        _data['sign'] = _sign
        self.render_json(**_data)


