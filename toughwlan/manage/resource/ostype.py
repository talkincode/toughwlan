#!/usr/bin/env python
# coding:utf-8

import cyclone.web
from toughlib import utils
from toughwlan.admin.base import BaseHandler, MenuRes
from toughlib.permit import permit
from toughwlan import models
from toughwlan.admin.resource import ostype_forms

permit.route(r"/ostype", u"终端类型管理", MenuRes, order=9.0001, is_menu=True)
class OsTypeHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.render("ostype_list.html", page_data=self.get_page_data(self.db.query(models.TrwOSTypes)))


permit.route(r"/ostype/add", u"终端类型新增", MenuRes, order=9.0002)
class AddHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.render("base_form.html", form=ostype_forms.ostype_add_form())

    @cyclone.web.authenticated
    def post(self):
        form = ostype_forms.ostype_add_form()
        if not form.validates(source=self.get_params()):
            self.render("base_form.html", form=form)
            return
        if self.db.query(models.TrwOSTypes.id).filter_by(match_rule=form.d.match_rule).count() > 0:
            self.render("base_form.html", form=form, msg=u"匹配规则已经存在")
            return

        ostype = models.TrwOSTypes()
        ostype.os_name = form.d.os_name
        ostype.dev_type = form.d.dev_type
        ostype.match_rule = form.d.match_rule
        self.db.add(ostype)

        ops_log = models.TrwOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)新增设备类型信息:%s' % (ops_log.operator_name, ostype.dev_type)
        self.db.add(ops_log)
        self.db.commit()
        self.redirect("/ostype",permanent=False)


permit.route(r"/ostype/update", u"终端类型修改", MenuRes, order=9.0003)
class UpdateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        ostype_id = self.get_argument("ostype_id")
        form = ostype_forms.ostype_update_form()
        form.fill(self.db.query(models.TrwOSTypes).get(ostype_id))
        return self.render("base_form.html", form=form)

    def post(self):
        form = ostype_forms.ostype_update_form()
        if not form.validates(source=self.get_params()):
            self.render("base_form.html", form=form)
            return
        ostype = self.db.query(models.TrwOSTypes).get(form.d.id)
        ostype.os_name = form.d.os_name
        ostype.dev_type = form.d.dev_type
        ostype.match_rule = form.d.match_rule

        ops_log = models.TrwOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)修改设备类型信息:%s' % (ops_log.operator_name, ostype.os_name)
        self.db.add(ops_log)

        self.db.commit()
        self.redirect("/ostype",permanent=False)


permit.route(r"/ostype/delete", u"终端类型删除", MenuRes, order=9.0003)
class DeleteHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        ostype_id = self.get_argument("ostype_id")
        self.db.query(models.TrwOSTypes).filter_by(id=ostype_id).delete()

        ops_log = models.TrwOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)删除设备类型信息:%s' % (ops_log.operator_name, ostype_id)
        self.db.add(ops_log)

        self.db.commit()
        self.redirect("/ostype",permanent=False)






