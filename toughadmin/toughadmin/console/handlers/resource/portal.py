#!/usr/bin/env python
# coding:utf-8
import cyclone.auth
import cyclone.escape
import cyclone.web

from toughadmin.common import utils
from toughadmin.console.handlers.base import BaseHandler, MenuRes
from toughadmin.common.permit import permit
from toughadmin.console import models
from toughadmin.console.handlers.resource import portal_form

portal_status = {0: u"正常", 1: u"未连接"}

@permit.route(r"/portal", u"Portal节点管理", MenuRes, order=3.0001, is_menu=True)
class PortalHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        portal_list = self.db.query(models.TraPortal)
        self.render("portal.html",
                    portal_list=portal_list,
                    portal_status=portal_status)

@permit.route(r"/portal/add", u"Portal节点新增", MenuRes, order=3.0002)
class AddHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.render("base_form.html", form=portal_form.portal_add_form())

    @cyclone.web.authenticated
    def post(self):
        form = portal_form.portal_add_form([])
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)
        if self.db.query(models.TraPortal.id).filter_by(ip_addr=form.d.ip_addr).count() > 0:
            return self.render("base_form.html", form=form, msg=u"ip地址已经存在")

        portal = models.TraPortal()
        portal.ip_addr = form.d.ip_addr
        portal.name = form.d.name
        portal.secret = form.d.secret
        portal.http_port = form.d.http_port
        portal.listen_port = form.d.listen_port
        portal.status = 0
        portal.last_check = utils.get_currtime()
        self.db.add(portal)

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)新增Portal信息:%s' % (ops_log.operator_name, portal.ip_addr)
        self.db.add(ops_log)

        self.db.commit()
        self.redirect("/portal", permanent=False)

@permit.route(r"/portal/update", u"Portal节点修改", MenuRes, order=3.0003)
class UpdateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        portal_id = self.get_argument("portal_id")
        portal = self.db.query(models.TraPortal).get(portal_id)
        form = portal_form.portal_update_form()
        form.fill(portal)
        return self.render("base_form.html", form=form)

    def post(self):
        form = portal_form.portal_update_form([])
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)

        portal = self.db.query(models.TraPortal).get(form.d.id)
        portal.name = form.d.name
        portal.secret = form.d.secret
        portal.http_port = form.d.http_port
        portal.listen_port = form.d.listen_port

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)修改Portal信息:%s' % (ops_log.operator_name, portal.ip_addr)
        self.db.add(ops_log)

        self.db.commit()
        self.redirect("/portal", permanent=False)

@permit.route(r"/portal/delete", u"Portal节点删除", MenuRes, order=3.0004, is_menu=False)
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



