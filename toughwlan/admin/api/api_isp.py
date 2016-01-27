#!/usr/bin/env python
# coding=utf-8

from toughlib.utils import safeunicode,get_currtime
from toughwlan.admin.api.api_base import ApiHandler
from toughlib.permit import permit
from toughwlan import models
import random

@permit.route(r"/api/isp/query")
class IspQueryHandler(ApiHandler):

    def get(self):
        self.post()

    def post(self):
        try:
            req_msg = self.parse_form_request()
            if 'isp_code' not in req_msg:
                raise ValueError("isp_code required")
        except Exception as err:
            self.render_result(code=1, msg=safeunicode(err.message))
            return

        isp = self.db.query(models.TrwIsp).filter_by(isp_code=req_msg['isp_code']).first()
        ispdata = { c.name : getattr(isp, c.name) for c in isp.__table__.columns}

        if not isp:
            self.render_result(code=1, msg="isp not exists")
        else:
            self.render_result(code=1, msg="success", data=ispdata)


@permit.route(r"/api/isp/register")
class IspRegisterHandler(ApiHandler):

    def next_isp_code(self):
        isp_code = str(random.randint(10000000,99999999))
        if self.db.query(models.TrwIsp.isp_code).filter_by(isp_code=isp_code).count() > 0:
            return self.next_isp_code()
        else:
            return isp_code

    def get(self):
        self.post()

    def post(self):
        try:
            req_msg = self.parse_form_request()
        except Exception as err:
            self.render_result(code=1, msg=safeunicode(err.message))
            return

        isp = models.TrwIsp()
        isp.isp_code = self.next_isp_code()
        isp.isp_name = req_msg.get("isp_name","")
        isp.isp_desc = req_msg.get("isp_desc","")
        isp.isp_email = req_msg.get("isp_email","")
        isp.isp_phone = req_msg.get("isp_phone","")
        isp.isp_idcard = req_msg.get("isp_idcard","")
        isp.user_total = 0
        isp.status = 0
        self.db.add(isp)
        self.db.commit()

        self.render_result(code=0, msg="success", data=dict(isp_code=isp.isp_code))


@permit.route(r"/api/isp/update")
class IspUpdateHandler(ApiHandler):
    
    def get(self):
        self.post()

    def post(self):
        try:
            req_msg = self.parse_form_request()
            if 'isp_code' not in req_msg:
                raise ValueError("isp_code required")
        except Exception as err:
            self.render_result(code=1, msg=safeunicode(err.message))
            return

        isp = self.db.query(models.TrwIsp).filter_by(isp_code=req_msg['isp_code']).first()
        if not isp:
            self.render_result(code=1, msg="isp not exists")
            return


        attrs = ['isp_name','isp_desc','isp_email','isp_phone','isp_idcard']

        for attr in attrs:
            if attr in req_msg:
                setattr(isp, attr, req_msg[attr])

        if 'status' in req_msg and req_msg['status'] in ('0','1'):
            isp.status = int(req_msg['status'])

        isp.isp_name = req_msg.get("isp_name","")
        isp.isp_desc = req_msg.get("isp_desc","")
        isp.isp_email = req_msg.get("isp_email","")
        isp.isp_phone = req_msg.get("isp_phone","")
        isp.isp_idcard = req_msg.get("isp_idcard","")
        self.db.commit()

        self.render_result(code=0, msg="success")



@permit.route(r"/api/isp/subscriber")
class IspServiceSubHandler(ApiHandler):

    def get(self):
        self.post()

    def post(self):
        try:
            req_msg = self.parse_form_request()
        except Exception as err:
            self.render_result(code=1, msg=safeunicode(err.message))
            return

        ispserv = models.TrwIspService()
        ispserv.isp_code = req_msg.get("isp_code")
        ispserv.service_type = req_msg.get("service_type")
        ispserv.sub_time = get_currtime()
        self.db.add(ispserv)
        self.db.commit()

        self.render_result(code=0, msg="success")


@permit.route(r"/api/isp/unsubscriber")
class IspServiceSubHandler(ApiHandler):

    def get(self):
        self.post()

    def post(self):
        try:
            req_msg = self.parse_form_request()
            if not all([req_msg.get("isp_code"),req_msg.get("service_type")]):
                raise ValueError("isp_code, service_type required")
        except Exception as err:
            self.render_result(code=1, msg=safeunicode(err.message))
            return

        self.db.query(models.TrwIspService).filter_by(
            isp_code = req_msg.get("isp_code"),
            service_type = req_msg.get("service_type")).delete()

        self.db.commit()

        self.render_result(code=0, msg="success")

