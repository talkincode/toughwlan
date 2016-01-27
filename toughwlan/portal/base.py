#!/usr/bin/env python
# coding:utf-8
import json
import re
import time
import urlparse
import urllib
import traceback
import functools
import cyclone.web
from mako.template import Template
from cyclone.util import ObjectDict
from twisted.internet import defer
from toughlib import utils, apiutils
from toughlib import dispatch, logger
from toughwlan import models
from toughlib import db_session as session

class BaseHandler(cyclone.web.RequestHandler):
    
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.cache = self.application.mcache
        self.session = session.Session(self.application.session_manager, self)


    def check_xsrf_cookie(self):
        pass

    def initialize(self):
        self.tp_lookup = self.application.tp_lookup
        self.db = self.application.db()
        
    def on_finish(self):
        self.db.close()
        
    def get_error_html(self, status_code=500, **kwargs):
        logger.info("http error : [status_code:{0}], {1}".format(status_code, utils.safestr(kwargs)))
        if status_code == 404:
            return self.render_string("error.html", msg=u"404:页面不存在")
        elif status_code == 403:
            return self.render_string("error.html", msg=u"403:非法的请求")
        elif status_code == 500:
            return self.render_string("error.html", msg=u"500:服务器处理失败，请联系管理员")
        else:
            return self.render_string("error.html", msg=u"%s:服务器处理失败，请联系管理员" % status_code)

    def render(self, template_name, **template_vars):
        html = self.render_string(template_name, **template_vars)
        self.write(html)

    def render_error(self, **template_vars):
        logger.info("render template error: {0}".format(repr(template_vars)))
        tpl_name = template_vars.get("tpl_name","")
        tpl = self.get_error_template(tpl_name)
        html = self.render_string(tpl, **template_vars)
        self.write(html)

    def render_json(self, **template_vars):
        if not template_vars.has_key("code"):
            template_vars["code"] = 0
        resp = json.dumps(template_vars, ensure_ascii=False)
        self.write(resp)


    def render_string(self, template_name, **template_vars):
        template_vars["xsrf_form_html"] = self.xsrf_form_html
        template_vars["current_user"] = self.current_user
        template_vars["login_time"] = self.get_secure_cookie("portal_logintime")
        template_vars["request"] = self.request
        template_vars["requri"] = "{0}://{1}".format(self.request.protocol, self.request.host)
        template_vars["handler"] = self
        template_vars["utils"] = utils
        try:
            mytemplate = self.tp_lookup.get_template(template_name)
            return mytemplate.render(**template_vars)
        except Exception as err:
            logger.info("Render template error {0}".format(utils.safestr(err)))
            raise

    def render_from_string(self, template_string, **template_vars):
        template = Template(template_string)
        return template.render(**template_vars)

    def set_session_user(self, username, ipaddr, login_time, **kwargs):
        session_user = ObjectDict()
        session_user.username = username
        session_user.ipaddr = ipaddr
        session_user.login_time = login_time
        session_user.update(**kwargs)
        self.session['session_user'] = session_user
        self.session.save()

    def clear_session(self):
        self.session.clear()
        self.session.save()
        self.clear_all_cookies()  
        
    def get_current_user(self):
        return self.session.get("session_user")


    def chk_os(self):
        chk_funcs = self.get_check_os_funs()
        def check_os(user_agent):
            for func in chk_funcs:
                if func[2].search(user_agent) is not None:
                    return func[0], func[1]
            return 'unknow', 'unknow'

        try:
            userAgent = self.request.headers['User-Agent']
            logger.info("UserAgent : %s"% userAgent)
            return check_os(userAgent)
        except:
            return 'unknow', 'unknow'


    def get_portal_name(self):
        return u"ToughWLAN"


    def get_wlan_params(self, query_str):
        query_str = urllib.unquote(query_str)
        params = urlparse.parse_qs(query_str)
        param_dict = {k: params[k][0] for k in params}
        return  param_dict

    def get_login_template(self, tpl_name=None):
        if tpl_name:
            return "%s/login.html" % tpl_name
        else:
            return "default/login.html"


    def get_error_template(self, tpl_path=None):
        if tpl_path:
            return "%s/error.html" % tpl_path
        else:
            return "default/error.html"

    def get_index_template(self, tpl_path=None):
        if tpl_path:
            return "%s/index.html" % tpl_path
        else:
            return "default/index.html"

    def get_template_attrs(self, ssid, ispcode):
        @self.cache.cache(prefix='portal', expire=600)  
        def _get_template_attrs(ssid,ispcode):
            domain_code = self.db.query(models.TrwSsid.domain_code).filter_by(
                ssid=ssid, isp_code=ispcode).scalar()
            tpl_name = self.db.query(models.TrwDomain.tpl_name).filter_by(
                domain_code=domain_code, isp_code=ispcode).scalar()
            tpl_name = tpl_name or "default"
            tpl_dict = dict(
                isp_code=ispcode,
                tpl_path=tpl_name,
                ssid=ssid,
                domain=domain_code
            )

            dmattrs = self.db.query(models.TrwDomainAttr).filter_by(
                domain_code=domain_code,isp_code=ispcode)
            for dattr in dmattrs:
                tpl_dict[dattr.attr_name] = dattr.attr_value

            return tpl_dict

        return _get_template_attrs(ssid,ispcode)

    def get_nas(self, ipaddr):
        @self.cache.cache(prefix='portal', expire=600)  
        def _get_nas_info(ipaddr):
            nas = self.db.query(models.TrwBas).filter_by(ip_addr=ipaddr).first()
            return nas and { c.name:getattr(nas, c.name)  for c in nas.__table__.columns} or {}
        return _get_nas_info(ipaddr)


    def get_domain(self, ssid, ispcode):
        @self.cache.cache(prefix='portal', expire=600)  
        def _get_domain_code(ssid,ispcode):
            return self.db.query(models.TrwSsid.domain_code).filter_by(
                ssid=ssid, isp_code=ispcode).scalar()
        return _get_domain_code(ssid,ispcode)

        
    def get_check_os_funs(self):
        @self.cache.cache(prefix='portal', expire=600)  
        def _get_check_os_funs():
            ostypes = [(it.os_name, it.dev_type, it.match_rule) for it in self.db.query(models.TrwOSTypes)]
            check_os_funcs = []
            for os_name, dev_type, rule in ostypes:
                check_os_funcs.append([dev_type, os_name, re.compile(r'{0}'.format(rule), re.IGNORECASE)])
            return check_os_funcs
        return _get_check_os_funs()







