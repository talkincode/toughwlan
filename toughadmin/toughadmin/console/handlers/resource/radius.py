#!/usr/bin/env python
# coding:utf-8
import cyclone.auth
import cyclone.escape
import cyclone.web

from toughadmin.common import utils
from toughadmin.console.handlers.base import BaseHandler, MenuRes
from toughadmin.common.permit import permit
from toughadmin.console.handlers.resource import radius_form
from toughadmin.console import models


@permit.route(r"/radius", u"Radius节点管理", MenuRes, order=2.0300, is_menu=True)
class RadiusHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        radius_list = self.db.query(models.TraRadius)
        self.render("radius.html",
                    radius_list=radius_list,
                    radius_status=radius_form.radius_status)

    def post(self):
        pass


@permit.route(r"/radius/detail", u"Radius节点详情", MenuRes, order=2.0302, is_menu=False)
class RadiusDetailHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        radius_name = self.get_argument("radius_name")
        status = self.db.query(models.TraStatus).filter_by(radius_name=radius_name).first()
        print status
        self.render("radius_detail.html",status=status)

    def post(self):
        pass


@permit.route(r"/radius/delete", u"Radius节点删除", MenuRes, order=2.0301, is_menu=False)
class RadiusDeleteHandler(BaseHandler):
    @cyclone.web.authenticated

    def get(self):
        radius_id = self.get_argument("radius_id")
        self.db.query(models.TraRadius).filter_by(id=radius_id).delete()

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)删除radius信息:%s' % (ops_log.operator_name, radius_id)
        self.db.add(ops_log)

        self.db.commit()
        self.redirect("/radius",permanent=False)






