#!/usr/bin/env python
# coding=utf-8

from toughlib.utils import safeunicode
from toughwlan.manage.api.api_base import ApiHandler
from toughlib.permit import permit
from toughwlan import models
import random

@permit.route(r"/api/nas/query")
class NasQueryHandler(ApiHandler):

    def get(self):
        self.post()

    def post(self):
        try:
            req_msg = self.parse_form_request()
        except Exception as err:
            self.render_result(code=1, msg=safeunicode(err.message))
            return

        nas_query = self.db.query(models.TrwBas)
        if req_msg.get('isp_code'):
            nas_query = nas_query.filter_by(isp_code=req_msg['isp_code'])

        result=[]
        for nas in nas_query:
            result.append({ c.name : getattr(nas, c.name) for c in nas.__table__.columns})

        self.render_result(code=0, msg="success", data=result)


@permit.route(r"/api/nas/add")
class NasAddHandler(ApiHandler):

    def get(self):
        self.post()

    def post(self):
        try:
            req_msg = self.parse_form_request()
            if 'isp_code' not in req_msg:
                raise ValueError("isp_code required")
            if  not any([req_msg.get('ip_addr'),req_msg.get("dns_name")]):
                raise ValueError("ip_addr, dns_name required one")
            if 'bas_secret' not in req_msg:
                raise ValueError("bas_secret required")
        except Exception as err:
            self.render_result(code=1, msg=safeunicode(err.message))
            return

        if self.db.query(models.TrwBas.id).filter_by(ip_addr=req_msg.get("ip_addr")).count() > 0:
            return self.render_result(code=1, msg=u"nas already exists")

        bas = models.TrwBas()
        bas.isp_code = req_msg.get("isp_code")
        bas.ip_addr = req_msg.get("ip_addr")
        bas.dns_name = req_msg.get("dns_name")
        bas.bas_name = req_msg.get("bas_name","new bas")
        bas.time_type = req_msg.get("time_type",0)
        bas.vendor_id = req_msg.get("vendor_id",0)
        bas.portal_vendor = req_msg.get("portal_vendor","huaweiv2")
        bas.bas_secret = req_msg.get("bas_secret")
        bas.coa_port = req_msg.get("coa_port",3799)
        bas.ac_port = req_msg.get("ac_port",2000)
        self.db.add(bas)
        self.db.commit()

        nasdata = { c.name : getattr(bas, c.name) for c in bas.__table__.columns}

        self.render_result(code=0, msg="success", data=nasdata)


@permit.route(r"/api/nas/update")
class NasUpdateHandler(ApiHandler):
    
    def get(self):
        self.post()

    def post(self):
        try:
            req_msg = self.parse_form_request()
            if  not any([req_msg.get('ip_addr'),req_msg.get("dns_name")]):
                raise ValueError("ip_addr, dns_name required one")
        except Exception as err:
            self.render_result(code=1, msg=safeunicode(err.message))
            return

        bas = self.db.query(models.TrwBas)
        if req_msg.get('ip_addr'):
            bas = bas.filter_by(ip_addr=req_msg['ip_addr']).first()
        elif req_msg.get('dns_name'):
            bas = bas.filter_by(dns_name=req_msg['dns_name']).first()

        if not bas:
            self.render_result(code=1, msg="nas not exists")
            return

        attrs = ['bas_name','time_type','vendor_id','portal_vendor','bas_secret','coa_port','ac_port']

        for attr in attrs:
            if attr in req_msg:
                setattr(bas, attr, req_msg[attr])

        self.db.commit()

        self.render_result(code=0, msg="success")


@permit.route(r"/api/nas/delete")
class NasDeleteHandler(ApiHandler):
    
    def get(self):
        self.post()

    def post(self):
        try:
            req_msg = self.parse_form_request()
            if  not any([req_msg.get('ip_addr'),req_msg.get("dns_name")]):
                raise ValueError("ip_addr, dns_name required one")
        except Exception as err:
            self.render_result(code=1, msg=safeunicode(err.message))
            return

        query = self.db.query(models.TrwBas)
        if req_msg.get('ip_addr'):
            query.filter_by(ip_addr=req_msg['ip_addr']).delete()
        elif req_msg.get('dns_name'):
            query.filter_by(dns_name=req_msg['dns_name']).delete()

        self.db.commit()

        self.render_result(code=0, msg="success")

