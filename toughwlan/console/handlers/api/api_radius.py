#!/usr/bin/env python
#coding=utf-8

from toughlib.utils import safestr
from toughwlan.console.handlers.api.api_base import ApiHandler
from toughlib.permit import permit
from toughwlan.console import models
from toughlib import utils
from toughwlan.console.handlers.resource import radius_form


@permit.route(r"/api/radius/ping")
class RadiusPingHandler(ApiHandler):
    """ radius 链路检测
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
        radius = self.db.query(models.TraRadius).filter_by(name=name, ip_addr=ipaddr).first()
        if not radius:
            return self.render_json(code=100, msg=u'radius node <{0}> not exists'.format(ipaddr))
        else:
            radius.last_check = utils.get_currtime()
            self.db.commit()

        return self.render_json(code=0, msg=u'pong')

