#!/usr/bin/env python
# coding:utf-8

import cyclone.web
from toughlib import utils
from toughwlan.console.handlers.base import BaseHandler,MenuRes
from toughlib.permit import permit
from toughwlan.console import models
from toughwlan.console.handlers.resource import nas_forms


@permit.route(r"/bas", u"接入设备管理", MenuRes, order=1.0000, is_menu=True)
class BasHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.render("bas_list.html",
                      bastype=nas_forms.bastype,
                      bas_list=self.db.query(models.TraBas))


@permit.route(r"/bas/add", u"接入设备新增", MenuRes, order=1.0001)
class AddHandler(BaseHandler):

    @cyclone.web.authenticated
    def get(self):
        self.render("base_form.html", form=nas_forms.bas_add_form())

    @cyclone.web.authenticated
    def post(self):
        form = nas_forms.bas_add_form()
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)
            
        if not any([form.d.ip_addr,form.d.dns_name]):
            return self.render("base_form.html", form=form, msg=u"ip地址或域名至少填写一项")

        if self.db.query(models.TraBas.id).filter_by(ip_addr=form.d.ip_addr).count() > 0:
            return self.render("base_form.html", form=form, msg=u"Bas地址已经存在")
            
        bas = models.TraBas()
        bas.ip_addr = form.d.ip_addr
        bas.dns_name = form.d.dns_name
        bas.bas_name = form.d.bas_name
        bas.time_type = form.d.time_type
        bas.vendor_id = form.d.vendor_id
        bas.portal_vendor = form.d.portal_vendor
        bas.bas_secret = form.d.bas_secret
        bas.coa_port = form.d.coa_port
        bas.ac_port = form.d.ac_port
        self.db.add(bas)

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)新增BAS信息:%s' % (ops_log.operator_name, bas.ip_addr)
        self.db.add(ops_log)
        self.db.commit()

        self.redirect("/bas",permanent=False)

@permit.route(r"/bas/update", u"接入设备修改", MenuRes, order=1.00002)
class UpdateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        bas_id = self.get_argument("bas_id")
        form = nas_forms.bas_update_form()
        form.fill(self.db.query(models.TraBas).get(bas_id))
        return self.render("base_form.html", form=form)

    def post(self):
        form = nas_forms.bas_update_form()
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)
            
        bas = self.db.query(models.TraBas).get(form.d.id)
        bas.bas_name = form.d.bas_name
        bas.dns_name = form.d.dns_name
        bas.time_type = form.d.time_type
        bas.vendor_id = form.d.vendor_id
        bas.portal_vendor = form.d.portal_vendor
        bas.bas_secret = form.d.bas_secret
        bas.coa_port = form.d.coa_port
        bas.ac_port = form.d.ac_port

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)修改BAS信息:%s' % (ops_log.operator_name, bas.ip_addr)
        self.db.add(ops_log)

        self.db.commit()

        self.redirect("/bas",permanent=False)

@permit.route(r"/bas/delete", u"接入设备删除", MenuRes, order=1.0003)
class DeleteHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        bas_id = self.get_argument("bas_id")
        self.db.query(models.TraBas).filter_by(id=bas_id).delete()

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)删除BAS信息:%s' % (ops_log.operator_name, bas_id)
        self.db.add(ops_log)

        self.db.commit()

        self.redirect("/bas",permanent=False)






