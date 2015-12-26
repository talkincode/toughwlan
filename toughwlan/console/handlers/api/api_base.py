#!/usr/bin/env python
# coding:utf-8
import json
from hashlib import md5

from twisted.python import log
from toughlib import utils, apiutils
from toughlib.utils import safestr
from toughwlan.console.handlers.base import BaseHandler
from toughlib.permit import permit
from toughwlan.console import models
import logging


class ApiHandler(BaseHandler):

    def check_xsrf_cookie(self):
        pass

    def parse_request(self):
        return apiutils.parse_request(self.settings.config.system.secret,self.request.body)
 

@permit.route(r"/api/oss/query")
class OssQueryHandler(ApiHandler):
    """ radius策略服务器配置信息获取
    """
    def post(self):
        try:
            req_msg = self.parse_request()
        except Exception as err:
            self.render_json(msg=safestr(err.message))
            return

        oss_server = self.db.query(models.TraOssServer).filter_by(status=1).first()

        pass

@permit.route(r"/api/tpl/query")
class TplQueryHandler(ApiHandler):
    """ 模板查询
    """
    def query_tpl_by_ssid(self,ssid):
        domain_code = self.db.query(models.TraSsid.domain_code).filter_by(ssid=ssid).scalar()
        tpl_name = self.db.query(models.TraDomain.tpl_name).filter_by(domain_code=domain_code).scalar()
        tpl_name = tpl_name or "default"
        tpl_dict = dict(
            tpl_name=tpl_name,
            bind_ssid=ssid,
            domain=domain_code
        )
        tpattrs = self.db.query(models.TraTemplateAttr).filter_by(tpl_name=tpl_name)
        for attr in tpattrs:
            tpl_dict[attr.attr_name] = attr.attr_value

        dmattrs = self.db.query(models.TraDomainAttr).filter_by(domain_code=domain_code)
        for dattr in dmattrs:
            tpl_dict[dattr.attr_name] = dattr.attr_value

        return dict(code=0, msg='success', attrs=tpl_dict)



    def post(self):
        try:
            req_msg = self.parse_request()
        except Exception as err:
            self.render_json(msg=safestr(err.message))
            return

        result = self.query_tpl_by_ssid(req_msg.get('ssid'))
        self.render_json(**result)


@permit.route(r"/api/domain/query")
class DomainQueryHandler(ApiHandler):
    """ 域信息查询
    """
    def query_domain_by_ssid(self,ssid):
        mssid = self.db.query(models.TraSsid).filter_by(ssid=ssid).first()
        if not mssid:
            log.msg("query domain : default")
            return dict(code=1, msg=u"ssid do not exist use default config", domain="default")

        log.msg("query domain :%s" %mssid.domain_code)
        return dict(code=0, msg='success',domain=mssid.domain_code)


    def query_domain_by_gwid(self, gwid):
        mgwid = self.db.query(models.TraGwid).filter_by(gwid=gwid).first()
        if not mgwid:
            log.msg("query domain : None")
            return dict(code=1, msg=u"gwid do not exist use default config", domain="")

        log.msg("query domain :%s" % mgwid.domain_code)
        return dict(code=0, msg='success', domain=mgwid.domain_code)


    def post(self):
        try:
            req_msg = self.parse_request()
        except Exception as err:
            self.render_json(msg=safestr(err.message))
            return
        ssid = req_msg.get('ssid')
        gwid = req_msg.get('gwid')
        if ssid:
            self.render_json(**self.query_domain_by_ssid(ssid))
        elif gwid:
            self.render_json(**self.query_domain_by_gwid(gwid))

@permit.route(r"/api/ostype/query")
class OSTypesQueryHandler(ApiHandler):
    """ 设备类型信息查询
    """
    def post(self):
        try:
            req_msg = self.parse_request()
        except Exception as err:
            self.render_json(msg=safestr(err.message))
            return

        ostypes = [(it.os_name, it.dev_type, it.match_rule) for it in self.db.query(models.TraOSTypes)]
        self.render_json(code=0, msg='success', rules=ostypes)

