#!/usr/bin/env python
# coding:utf-8
import cyclone.web
from toughwlan.admin.base import BaseHandler
from toughlib.permit import permit
from toughlib import utils
from toughwlan.admin.system import config_forms
from toughwlan import models


@permit.route(r"/config", u"参数配置管理", u"系统管理", order=2.0000, is_menu=True)
class ConfigHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        active = self.get_argument("active", "default")
        default_form = config_forms.default_form()
        default_form.fill(self.settings.config.system)
        syslog_form = config_forms.syslog_form()
        syslog_form.fill(self.settings.config.syslog)
        database_form = config_forms.database_form()
        database_form.fill(self.settings.config.database)        
        portal_form = config_forms.portal_form()
        portal_form.fill(self.settings.config.portal)
        admin_form = config_forms.admin_form()
        admin_form.fill(self.settings.config.admin)

        paramDict = {}
        params = self.db.query(models.TrwParam).all()

        for param in params:
            paramDict[param.param_name] = param.param_value


        self.render("config.html",
                  active=active,
                  default_form=default_form,
                  database_form=database_form,
                  portal_form=portal_form,
                  admin_form=admin_form,
                  syslog_form=syslog_form
              )

@permit.route(r"/config/default/update", u"默认配置", u"系统管理", order=2.0001, is_menu=False)
class DefaultHandler(BaseHandler):
    @cyclone.web.authenticated
    def post(self):
        self.settings.config['system']['debug'] = int(self.get_argument("debug"))
        self.settings.config['system']['tz'] = utils.safestr(self.get_argument("tz"))
        self.settings.config.save()
        self.redirect("/config?active=default")

@permit.route(r"/config/database/update", u"数据库配置", u"系统管理", order=2.0002, is_menu=False)
class DatabaseHandler(BaseHandler):
    @cyclone.web.authenticated
    def post(self):
        config = self.settings.config
        config['database']['echo'] = int(self.get_argument("echo"))
        config['database']['dbtype'] = self.get_argument("dbtype")
        config['database']['dburl'] = self.get_argument("dburl")
        config['database']['pool_size'] = int(self.get_argument("pool_size"))
        config['database']['pool_recycle'] = int(self.get_argument("pool_recycle"))
        config['database']['backup_path'] = self.get_argument("backup_path")
        config.save()
        self.redirect("/config?active=database")

@permit.route(r"/config/portal/update", u"Portal 配置", u"系统管理", order=2.0003, is_menu=False)
class PortalHandler(BaseHandler):
    @cyclone.web.authenticated
    def post(self):
        config = self.settings.config
        config['portal']['secret'] = self.get_argument("secret")
        config['portal']['vendor'] = self.get_argument("vendor")
        config.save()
        self.redirect("/config?active=portal")

@permit.route(r"/config/syslog/update", u"syslog 配置", u"系统管理", order=2.0004, is_menu=False)
class SyslogHandler(BaseHandler):
    @cyclone.web.authenticated
    def post(self):
        config = self.settings.config
        config['syslog']['enable'] = int(self.get_argument("enable"))
        config['syslog']['server'] = self.get_argument("server")
        config['syslog']['port'] = int(self.get_argument("port",514))
        config['syslog']['level'] = self.get_argument("level")
        config.save()
        self.application.syslog.setup(config)
        self.redirect("/config?active=syslog")


