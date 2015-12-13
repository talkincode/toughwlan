#!/usr/bin/env python
#coding=utf-8
import time

from toughadmin.common import utils
from toughadmin.common.permit import permit
from toughadmin.console.handlers.api import api_base
from toughadmin.console import models


@permit.route(r"/api/nas/fetch")
class NasFetchHandler(api_base.ApiHandler):

    def get(self):
        self.post()

    def post(self):
        try:
            req_msg = self.parse_request()
            if 'nasaddr' not in req_msg:
                raise ValueError("nasaddr is empty")
        except Exception as err:
            self.render_json(code=1, msg=utils.safestr(err.message))
            return

        nasaddr = req_msg['nasaddr']
        nas = self.db.query(models.TraBas).filter_by(ip_addr=nasaddr).first()
        if not nas:
            self.render_json(code=1, msg='nas {0} not exists'.format(nasaddr))
            return

        api_addr = self.settings.config.admin.api_addr
        api_port = self.settings.config.admin.port

        result = {
            'code'        : 0,
            'msg'         : 'ok',
            'ipaddr'      : nasaddr,
            'secret'      : nas.bas_secret,
            'vendor_id'   : nas.vendor_id,
            'coa_port'    : int(nas.coa_port or 3799),
            'ac_port'     : int(nas.ac_port or 2000),
            'api_secret'  : self.settings.config.defaults.secret,
            'api_auth_url': "http://{0}:{1}/api/authorize".format(api_addr,api_port),
            'api_acct_url': "http://{0}:{1}/api/acctounting".format(api_addr, api_port),
            'nonce'       : str(int(time.time())),
        }

        result['sign'] = api_base.mksign(self.settings.config.defaults.secret, result.values())
        self.render_json(**result)



