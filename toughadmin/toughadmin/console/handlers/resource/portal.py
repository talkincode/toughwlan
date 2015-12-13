#!/usr/bin/env python
# coding:utf-8
import cyclone.auth
import cyclone.escape
import cyclone.web

from toughadmin.common import utils
from toughadmin.console.handlers.base import BaseHandler, MenuRes
from toughadmin.common.permit import permit
from toughadmin.console import models

portal_status = {0: u"正常", 1: u"未连接"}

@permit.route(r"/portal", u"Portal节点管理", MenuRes, order=3.0001, is_menu=True)
class PortalHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        portal_list = self.db.query(models.TraPortal)
        self.render("portal.html",
                    portal_list=portal_list,
                    portal_status=portal_status)

    def post(self):
        pass

@permit.route(r"/portal/delete", u"Portal节点删除", MenuRes, order=3.0002, is_menu=False)
class PortalDeleteHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        portal_id = self.get_argument("portal_id")
        self.db.query(models.TraPortal).filter_by(id=portal_id).delete()

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)删除portal信息:%s' % (ops_log.operator_name, portal_id)
        self.db.add(ops_log)

        self.db.commit()
        self.redirect("/portal",permanent=False)



