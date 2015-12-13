#!/usr/bin/env python
# coding:utf-8

import cyclone.auth
import cyclone.escape
import cyclone.web

from toughadmin.common import utils
from toughadmin.console.handlers.base import BaseHandler, MenuRes
from toughadmin.common.permit import permit
from toughadmin.console import models
from toughadmin.console.handlers.resource import ssid_form

@permit.route(r"/ssid", u"SSID信息管理", MenuRes, order=6.0000, is_menu=True)
class SsidHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.render("ssid_list.html",
                      page_data=self.get_page_data(self.db.query(models.TraSsid)))


@permit.route(r"/ssid/add", u"SSID信息新增", MenuRes, order=6.0001)
class AddHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        domains = [(m.domain_code, m.domain_desc) for m in self.db.query(models.TraDomain)]
        self.render("base_form.html", form=ssid_form.ssid_add_form(domains))

    @cyclone.web.authenticated
    def post(self):
        form = ssid_form.ssid_add_form([])
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)
        if self.db.query(models.TraSsid.id).filter_by(ssid=form.d.ssid).count() > 0:
            return self.render("base_form.html", form=form, msg=u"ssid已经存在")
        mssid = models.TraSsid()
        mssid.domain_code = form.d.domain_code
        mssid.ssid = form.d.ssid
        mssid.ssid_desc = form.d.ssid_desc
        self.db.add(mssid)

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)新增SSID信息:%s' % (ops_log.operator_name, mssid.ssid)
        self.db.add(ops_log)

        self.db.commit()
        self.redirect("/ssid",permanent=False)


@permit.route(r"/ssid/update", u"SSID信息修改", MenuRes, order=6.0002)
class UpdateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        domains = [(m.domain_code, m.domain_desc) for m in self.db.query(models.TraDomain)]
        ssid_id = self.get_argument("ssid_id")
        mssid = self.db.query(models.TraSsid).get(ssid_id)
        form = ssid_form.ssid_update_form(domains)
        form.fill(mssid)
        return self.render("base_form.html", form=form)

    def post(self):
        form = ssid_form.ssid_update_form([])
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)
        mssid = self.db.query(models.TraSsid).get(form.d.id)
        mssid.domain_code = form.d.domain_code
        mssid.ssid_desc = form.d.ssid_desc

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)修改SSID信息:%s' % (ops_log.operator_name, mssid.ssid)
        self.db.add(ops_log)

        self.db.commit()
        self.redirect("/ssid",permanent=False)

@permit.route(r"/ssid/delete", u"SSID信息删除", MenuRes, order=6.0003)
class DeleteHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        ssid_id = self.get_argument("ssid_id")
        self.db.query(models.TraSsid).filter_by(id=ssid_id).delete()

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)删除SSID信息:%s' % (ops_log.operator_name, ssid_id)
        self.db.add(ops_log)

        self.db.commit()
        self.redirect("/ssid",permanent=False)






