#!/usr/bin/env python
# coding=utf-8

from toughlib.utils import safeunicode
from toughwlan.admin.api.api_base import ApiHandler
from toughlib.permit import permit
from toughwlan import models

@permit.route(r"/api/radius/query")
class RadiusQueryHandler(ApiHandler):

    def get(self):
        self.post()

    def post(self):
        try:
            req_msg = self.parse_form_request()
        except Exception as err:
            self.render_result(code=1, msg=safeunicode(err.message))
            return

        result = []
        for radius in self.db.query(models.TrwRadius):
            result.append(dict(
                ip_addr=radius.ip_addr,
                name=radius.name,
                secret=radius.secret,
                auth_port=radius.auth_port,
                acct_port=radius.acct_port
            ))

        self.render_result(code=0, msg="success", data=result)







