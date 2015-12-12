#!/usr/bin/env python
#coding=utf-8

from toughadmin.common.utils import safestr
from toughadmin.console.handlers.api.api_base import ApiHandler
from toughadmin.common.permit import permit
from toughadmin.console import models
from toughadmin.common import utils
from toughadmin.console.handlers.resource import radius_form


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
        ipaddr = req_msg.get('ip_addr') or self.request.remote_ip

        # check radius exists
        radius = self.db.query(models.TraRadius).filter_by(name=name, ip_addr=ipaddr).first()
        if not radius:
            return self.render_json(code=100, msg=u'radius node not exists')
        else:
            radius.last_check = utils.get_currtime()
            self.db.commit()

        return self.render_json(code=0, msg=u'pong')

@permit.route(r"/api/radius/status")
class StatusReportHandler(ApiHandler):
    """ radius 状态上报
    """
    def post(self):
        try:
            req_msg = self.parse_request()
        except Exception as err:
            self.render_json(msg=safestr(err.message))
            return

        name = req_msg.get('name')
        auth_all = req_msg.get('auth_all')
        auth_accept = req_msg.get('auth_accept')
        auth_reject = req_msg.get('auth_reject')
        acct_all = req_msg.get('acct_all')
        acct_start = req_msg.get('acct_start')
        acct_stop = req_msg.get('acct_stop')
        acct_update = req_msg.get('acct_update')
        acct_on = req_msg.get('acct_on')
        acct_off = req_msg.get('acct_off')

        status = self.db.query(models.TraStatus).filter_by(radius_name=name).first()
        if not status:
            stat = models.TraStatus()
            stat.radius_name = name
            stat.auth_all = auth_all
            stat.auth_accept = auth_accept
            stat.auth_reject = auth_reject
            stat.acct_all = acct_all
            stat.acct_start = acct_start
            stat.acct_stop = acct_stop
            stat.acct_update = acct_update
            stat.acct_on = acct_on
            stat.acct_off = acct_off
            self.db.add(stat)
        else:
            status.auth_all = auth_all
            status.auth_accept = auth_accept
            status.auth_reject = auth_reject
            status.acct_all = acct_all
            status.acct_start = acct_start
            status.acct_stop = acct_stop
            status.acct_update = acct_update
            status.acct_on = acct_on
            status.acct_off = acct_off

        self.db.commit()
        return self.render_json(code=0, msg=u'success')


@permit.route(r"/api/radius/add")
class RadiusAddHandler(ApiHandler):
    """ radius 接入
    """

    def post(self):
        try:
            req_msg = self.parse_request()
        except Exception as err:
            self.render_json(msg=safestr(err.message))
            return

        name = req_msg.get('name')
        ip_addr = req_msg.get('ip_addr') or self.request.remote_ip
        admin_port = req_msg.get('admin_port')
        secret = req_msg.get('secret')
        auth_port = req_msg.get('auth_port')
        acct_port = req_msg.get('acct_port')

        vform = radius_form.radius_add_vform()
        if not vform.validates(dict(
            name=name,
            ip_addr=ip_addr,
            admin_port=admin_port,
            secret=secret,
            auth_port=auth_port,
            acct_port=acct_port)):
            return self.render_json(code=1, msg=vform.errors)

        radius = models.TraRadius()
        radius.name = name
        radius.ip_addr = ip_addr
        radius.secret = secret
        radius.admin_port = admin_port
        radius.auth_port = auth_port
        radius.acct_port = acct_port
        radius.status = 0
        radius.last_check = utils.get_currtime()

        self.db.add(radius)
        self.db.commit()
        return self.render_json(code=0, msg=u'success')
