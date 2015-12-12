#!/usr/bin/env python
# coding:utf-8

import cyclone.auth
import cyclone.escape
import cyclone.web

from toughadmin.common import utils
from toughadmin.console.handlers.base import BaseHandler, MenuRes
from toughadmin.common.permit import permit
from toughadmin.console import models
from toughadmin.console.handlers.resource import oss_server_forms


@permit.route(r"/oss", u"OSS服务器管理", MenuRes, order=2.0200, is_menu=True)
class OssServerHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.render("oss_server_list.html",oss_status=oss_server_forms.boolean,
                      oss_server_list=self.db.query(models.TraOssServer))

@permit.route(r"/oss/add", u"OSS服务器新增", MenuRes, order=2.0201, is_menu=False)
class AddHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.render("base_form.html", form=oss_server_forms.oss_add_form())

    @cyclone.web.authenticated
    def post(self):
        form = oss_server_forms.oss_add_form()
        if not form.validates(source=self.get_params()):
            self.render("base_form.html", form=form)
            return
        if self.db.query(models.TraOssServer).filter_by(oss_server_ip=form.d.oss_server_ip).count() > 0:
            self.render("base_form.html", form=form, msg=u"策略服务器已经存在")
            return
        oss_server = models.TraOssServer()
        oss_server.oss_server_ip = form.d.oss_server_ip
        oss_server.oss_auth_port = form.d.oss_auth_port
        oss_server.oss_acct_port = form.d.oss_acct_port
        oss_server.status = form.d.status
        oss_server.secret = form.d.secret
        self.db.add(oss_server)

        if form.d.status == '1':
            self.db.query(models.TraOssServer).filter(models.TraOssServer.oss_server_ip != form.d.oss_server_ip).update({'status':0})

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)新增策略服务器信息:%s' % (ops_log.operator_name, oss_server.oss_server_ip)
        self.db.add(ops_log)
        self.db.commit()

        self.redirect("/oss",permanent=False)


@permit.route(r"/oss/update", u"策略服务器修改", MenuRes, order=2.0202, is_menu=False)
class UpdateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        oss_id = self.get_argument("oss_id")
        oss_server = self.db.query(models.TraOssServer).get(oss_id)
        form = oss_server_forms.oss_update_form()
        form.fill(oss_server)
        return self.render("base_form.html", form=form)

    def post(self):
        form = oss_server_forms.oss_update_form()
        if not form.validates(source=self.get_params()):
            self.render("base_form.html", form=form)
            return
        oss_server = self.db.query(models.TraOssServer).get(form.d.id)
        oss_server.oss_server_ip = form.d.oss_server_ip
        oss_server.oss_auth_port = form.d.oss_auth_port
        oss_server.oss_acct_port = form.d.oss_acct_port
        oss_server.secret = form.d.secret

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)修改策略服务器信息:%s' % (ops_log.operator_name, oss_server.oss_server_ip)
        self.db.add(ops_log)
        self.db.commit()

        self.redirect("/oss",permanent=False)


@permit.route(r"/oss/delete", u"策略服务器删除", MenuRes, order=2.0203, is_menu=False)
class DeleteHandler(BaseHandler):
    @cyclone.web.authenticated
    def post(self):
        oss_id = self.get_argument("oss_id")

        oss_server = self.db.query(models.TraOssServer).filter(models.TraOssServer.id==oss_id,
                                                                     models.TraOssServer.status==1).first()

        if oss_server:
            self.render_json(code=1, msg=u"此策略服务器正处于活动状态,不允许删除")
            return

        self.db.query(models.TraOssServer).filter_by(id=oss_id).delete()

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)删除策略服务器信息:%s' % (ops_log.operator_name, oss_id)
        self.db.add(ops_log)
        self.db.commit()

        self.render_json(code=0,msg=u'success')

@permit.route(r"/oss/activate", u"OSS服务器激活", MenuRes, order=2.0204, is_menu=False)
class ActivateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        oss_id = self.get_argument("oss_id")
        self.db.query(models.TraOssServer).filter(id!=oss_id).update({'status':0})
        oss_server = self.db.query(models.TraOssServer).filter_by(id=oss_id).first()
        oss_server.status = 1

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)激活策略服务器信息:%s' % (ops_log.operator_name, oss_id)
        self.db.add(ops_log)
        self.db.commit()

        self.redirect("/oss",permanent=False)






