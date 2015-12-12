#!/usr/bin/env python
# coding=utf-8

from toughengine.radiusd.console.base import BaseHandler
from toughengine.radiusd.utils import safestr

class AuthHandler(BaseHandler):
    """ authorize handler"""
    def post(self):
        """ authorize post
        :return: :rtype:
        """
        try:
            req_msg = self.parse_request()
        except Exception as err:
            self.render_json(msg=safestr(err.message))
            return

        result = dict(
            code=0,
            msg=u'success',
            username=req_msg['username'],
            passwd='123456',
            input_rate=4194304,
            output_rate=4194304,
            attrs={
                "Session-Timeout": 3600,
                "Acct-Interim-Interval": 300
            }
        )

        sign = self.make_sign(self.settings.api_secret,result.values())
        result['sign'] = sign
        self.render_json(**result)


class AcctHandler(BaseHandler):
    """ accounting handler"""

    def post(self):
        """ accounting post
        :return: :rtype:
        """
        try:
            req_msg = self.parse_request()
        except Exception as err:
            self.render_json(msg=safestr(err.message))
            return

        result = dict(
            code=0,
            msg=u'success',
            username=req_msg['username']
        )

        sign = self.make_sign(self.settings.api_secret,result.values())
        result['sign'] = sign
        self.render_json(**result)










