#!/usr/bin/env python
#coding=utf-8

from toughadmin.common.utils import safestr
from toughadmin.console.handlers.api.api_base import ApiHandler
from toughadmin.common.permit import permit
from toughadmin.console import models
from toughadmin.common import utils
from toughadmin.console.handlers.resource import portal_form


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
        ipaddr = req_msg.get('ip_addr') or self.request.remote_ip

        # check radius exists
        portal = self.db.query(models.TraPortal).filter_by(name=name, ip_addr=ipaddr).first()
        if not portal:
            return self.render_json(code=100, msg=u'portal node not exists')
        else:
            portal.last_check = utils.get_currtime()
            self.db.commit()

        return self.render_json(code=0, msg=u'pong')

@permit.route(r"/api/portal/add")
class PortalAddHandler(ApiHandler):
    """ portal 接入
    """
    def post(self):
        try:
            req_msg = self.parse_request()
        except Exception as err:
            self.render_json(msg=safestr(err.message))
            return

        name = req_msg.get('name')
        ip_addr = req_msg.get('ip_addr') or self.request.remote_ip

        if self.db.query(models.TraPortal).filter_by(name=name, ip_addr=ip_addr).count() > 0:
            return self.render_json(code=0, msg=u'portal exists')

        secret = req_msg.get('secret')
        http_port = req_msg.get('http_port')
        listen_port = req_msg.get('listen_port')

        vform = portal_form.portal_add_vform()
        _data = dict(
            name=name,
            ip_addr=ip_addr,
            secret=secret,
            http_port=http_port,
            listen_port=listen_port
        )

        if not vform.validates(_data):
            return self.render_json(code=1, msg=vform.errors)

        portal = models.TraPortal()
        portal.name = name
        portal.ip_addr = ip_addr
        portal.secret = secret
        portal.http_port = http_port
        portal.listen_port = listen_port
        portal.status = 0
        portal.last_check = utils.get_currtime()

        self.db.add(portal)
        self.db.commit()
        return self.render_json(code=0, msg=u'success')

