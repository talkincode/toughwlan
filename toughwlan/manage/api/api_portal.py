#!/usr/bin/env python
# coding=utf-8

from toughlib.utils import safeunicode
from toughwlan.admin.api.api_base import ApiHandler
from toughlib.permit import permit
from toughwlan import models

@permit.route(r"/api/portal/query")
class PortalQueryHandler(ApiHandler):

    def get(self):
        self.post()

    def post(self):
        try:
            req_msg = self.parse_form_request()
        except Exception as err:
            self.render_result(code=1, msg=safeunicode(err.message))
            return

        result = dict(
            portal_addr=self.settings.config.portal.proxy_addr,
            portal_listen=self.settings.config.portal.listen
        )

        self.render_result(code=0, msg="success", data=result)







