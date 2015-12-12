#!/usr/bin/env python
# coding:utf-8
import cyclone.auth
import cyclone.escape
import cyclone.web

from toughadmin.common import utils
from toughadmin.console.handlers.base import BaseHandler, MenuUser
from toughadmin.common.permit import permit
from toughadmin.console import models

@permit.route(r"/online", u"用户会话管理", MenuUser, order=2.0810, is_menu=True)
class OnlineHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        online_list = self.db.query(models.TraOnline)
        self.render("online_list.html", page_data=self.get_page_data(online_list))

    def post(self):
        pass

@permit.route(r"/online/delete", u"用户解锁", MenuUser, order=2.0811, is_menu=False)
class OnlineDeleteHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        session_id = self.get_argument("session_id")
        self.db.query(models.TraOnline).filter_by(session_id=session_id).delete()

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)解锁用户会话:%s' % (ops_log.operator_name, session_id)
        self.db.add(ops_log)

        self.db.commit()
        self.redirect("/online",permanent=False)



