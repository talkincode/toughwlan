#!/usr/bin/env python
# coding=utf-8

from toughadmin.common import utils
from toughadmin.common.permit import permit
from toughadmin.console.handlers.api import api_base
from toughadmin.console import models


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

        sign = api_base.mksign(self.settings.config.defaults.secret, result.values())
        result['sign'] = sign
        self.render_json(**result)