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


class SsidHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.render("ssid_list.html",
                      page_data=self.get_page_data(self.db.query(models.TraSsid)))



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


permit.add_route(SsidHandler, r"/ssid", u"SSID信息管理", MenuRes, order=2.0600, is_menu=True)
permit.add_route(AddHandler, r"/ssid/add", u"SSID信息新增", MenuRes, order=2.0601, is_menu=False)
permit.add_route(UpdateHandler, r"/ssid/update", u"SSID信息修改", MenuRes, order=2.0602, is_menu=False)
permit.add_route(DeleteHandler, r"/ssid/delete", u"SSID信息删除", MenuRes, order=2.0603, is_menu=False)
