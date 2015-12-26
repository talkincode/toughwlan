#!/usr/bin/env python
# coding=utf-8

from toughlib import utils, apiutils
from toughlib.permit import permit
from toughwlan.console.handlers.api import api_base
from toughwlan.console import models


@permit.route(r"/api/acctounting")
class AcctountingHandler(api_base.ApiHandler):
    """ accounting handler"""

    def post(self):
        try:
            req_msg = self.parse_request()
            if 'username' not in req_msg:
                raise ValueError('username is empty')
        except Exception as err:
            self.render_json(msg=utils.safestr(err.message))
            return

        username = req_msg['username']

        result = dict(
            code=0,
            msg=u'success',
            username=username
        )

        sign = apiutils.mksign(self.settings.config.system.secret, result.values())
        result['sign'] = sign
        self.render_json(**result)