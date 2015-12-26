#!/usr/bin/env python
# coding:utf-8
import ConfigParser

import cyclone.auth
import cyclone.escape
import cyclone.web

from toughwlan.console.handlers.base import BaseHandler
from toughlib.permit import permit
from toughlib import utils
from toughwlan.console.handlers.system import config_forms
from toughwlan.console import models


@permit.route(r"/config", u"参数配置管理", u"系统管理", order=2.0000, is_menu=True)
class ConfigHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        active = self.get_argument("active", "default")
        default_form = config_forms.default_form()
        default_form.fill(self.settings.config.system)
        database_form = config_forms.database_form()
        database_form.fill(self.settings.config.database)
        admin_form = config_forms.admin_form()
        admin_form.fill(self.settings.config.admin)

        paramDict = {}
        params = self.db.query(models.TraParam).all()

        for param in params:
            paramDict[param.param_name] = param.param_value


        self.render("config.html",
                  active=active,
                  default_form=default_form,
                  database_form=database_form,
                  admin_form=admin_form
              )

@permit.route(r"/config/default/update", u"默认配置", u"系统管理", order=2.0001, is_menu=False)
class DefaultHandler(BaseHandler):
    @cyclone.web.authenticated
    def post(self):
        sys_config = self.settings.config.system
        _config = dict(
            debug=int(self.get_argument("debug")),
            tz=utils.safestr(self.get_argument("tz"))
        )
        sys_config.update(_config)
        self.settings.config.update(system=sys_config)
        self.settings.config.save()
        self.redirect("/config?active=default")

@permit.route(r"/config/database/update", u"数据库配置", u"系统管理", order=2.0002, is_menu=False)
class DatabaseHandler(BaseHandler):
    @cyclone.web.authenticated
    def post(self):
        config = self.settings.config
        config.database.echo = self.get_argument("echo")
        config.database.dbtype = self.get_argument("dbtype")
        config.database.dburl = self.get_argument("dburl")
        config.database.pool_size = self.get_argument("pool_size")
        config.database.pool_recycle = self.get_argument("pool_recycle")
        config.database.backup_path = self.get_argument("backup_path")
        config.save()
        self.redirect("/config?active=database")


