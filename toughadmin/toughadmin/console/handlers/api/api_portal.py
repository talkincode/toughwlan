#!/usr/bin/env python
#coding=utf-8

from toughadmin.common.utils import safestr
from toughadmin.console.handlers.api.api_base import ApiHandler
from toughadmin.common.permit import permit
from toughadmin.console import models
from toughadmin.common import utils


@permit.route(r"/api/portal/ping")
class PortalPingHandler(ApiHandler):
    """ portal 链路检测
    """
    def post(self):
        try:
            req_msg = self.parse_request()
        except Exception as err:
            self.render_json(msg=safestr(err.message))
            return

        name = req_msg.get('name')
        ipaddr = req_msg.get('ipaddr') or self.request.remote_ip

        # check radius exists
        portal = self.db.query(models.TraPortal).filter_by(name=name, ip_addr=ipaddr).first()
        if not portal:
            return self.render_json(code=100, msg=u'portal node not exists')
        else:
            portal.last_check = utils.get_currtime()
            self.db.commit()

        return self.render_json(code=0, msg=u'pong')


