#!/usr/bin/env python
# coding:utf-8
import cyclone.auth
import cyclone.escape
import cyclone.web

from toughadmin.common import utils
from toughadmin.console.handlers.base import BaseHandler, MenuRes
from toughadmin.common.permit import permit
from toughadmin.console import models
from toughadmin.console.handlers.resource import ostype_forms


class OsTypeHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.render("ostype_list.html", page_data=self.get_page_data(self.db.query(models.TraOSTypes)))

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
        if self.db.query(models.TraOSTypes.id).filter_by(match_rule=form.d.match_rule).count() > 0:
            self.render("base_form.html", form=form, msg=u"匹配规则已经存在")
            return

        ostype = models.TraOSTypes()
        ostype.os_name = form.d.os_name
        ostype.dev_type = form.d.dev_type
        ostype.match_rule = form.d.match_rule
        self.db.add(ostype)

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)新增设备类型信息:%s' % (ops_log.operator_name, ostype.dev_type)
        self.db.add(ops_log)
        self.db.commit()
        self.redirect("/ostype",permanent=False)


class UpdateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        ostype_id = self.get_argument("ostype_id")
        form = ostype_forms.ostype_update_form()
        form.fill(self.db.query(models.TraOSTypes).get(ostype_id))
        return self.render("base_form.html", form=form)

    def post(self):
        form = ostype_forms.ostype_update_form()
        if not form.validates(source=self.get_params()):
            self.render("base_form.html", form=form)
            return
        ostype = self.db.query(models.TraOSTypes).get(form.d.id)
        ostype.os_name = form.d.os_name
        ostype.dev_type = form.d.dev_type
        ostype.match_rule = form.d.match_rule

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)修改设备类型信息:%s' % (ops_log.operator_name, ostype.os_name)
        self.db.add(ops_log)

        self.db.commit()
        self.redirect("/ostype",permanent=False)


class DeleteHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        ostype_id = self.get_argument("ostype_id")
        self.db.query(models.TraOSTypes).filter_by(id=ostype_id).delete()

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)删除设备类型信息:%s' % (ops_log.operator_name, ostype_id)
        self.db.add(ops_log)

        self.db.commit()
        self.redirect("/ostype",permanent=False)



permit.add_route(OsTypeHandler, r"/ostype", u"终端类型管理", MenuRes, order=2.0400, is_menu=True)
permit.add_route(AddHandler, r"/ostype/add", u"终端类型新增", MenuRes, order=2.0401, is_menu=False)
permit.add_route(UpdateHandler, r"/ostype/update", u"终端类型修改", MenuRes, order=2.0402, is_menu=False)
permit.add_route(DeleteHandler, r"/ostype/delete", u"终端类型删除", MenuRes, order=2.0402, is_menu=False)