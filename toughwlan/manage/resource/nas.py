#!/usr/bin/env python
# coding:utf-8

import cyclone.web
from toughlib import utils
from toughwlan.manage.base import BaseHandler,MenuRes
from toughlib.permit import permit
from toughwlan import models
from toughwlan.manage.resource import nas_forms


@permit.route(r"/bas", u"接入设备管理", MenuRes, order=1.0000, is_menu=True)
class BasHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.render("bas_list.html",
                      bastype=nas_forms.bastype,
                      bas_list=self.db.query(models.TrwBas))


@permit.route(r"/bas/add", u"接入设备新增", MenuRes, order=1.0001)
class AddHandler(BaseHandler):

    @cyclone.web.authenticated
    def get(self):
        isps = [(t.isp_code, t.isp_name) for t in self.db.query(models.TrwIsp)]
        self.render("base_form.html", form=nas_forms.bas_add_form(isps=isps))

    @cyclone.web.authenticated
    def post(self):
        isps = [(t.isp_code, t.isp_name) for t in self.db.query(models.TrwIsp)]
        form = nas_forms.bas_add_form(isps)
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)
            
        if not any([form.d.ip_addr,form.d.dns_name]):
            return self.render("base_form.html", form=form, msg=u"ip地址或域名至少填写一项")

        if self.db.query(models.TrwBas.id).filter_by(ip_addr=form.d.ip_addr).count() > 0:
            return self.render("base_form.html", form=form, msg=u"Bas地址已经存在")
            
        bas = models.TrwBas()
        bas.isp_code = form.d.isp_code
        bas.ip_addr = form.d.ip_addr
        bas.dns_name = form.d.dns_name
        bas.bas_name = form.d.bas_name
        bas.time_type = form.d.time_type
        bas.vendor_id = form.d.vendor_id
        bas.portal_vendor = form.d.portal_vendor
        bas.bas_secret = form.d.bas_secret
        bas.coa_port = form.d.coa_port
        bas.ac_port = form.d.ac_port
        self.db.add(bas)

        self.add_oplog(u'新增BAS信息:%s' % ( bas.ip_addr))
        self.db.commit()

        self.redirect("/bas",permanent=False)

@permit.route(r"/bas/update", u"接入设备修改", MenuRes, order=1.00002)
class UpdateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        bas_id = self.get_argument("bas_id")
        isps = [(t.isp_code, t.isp_name) for t in self.db.query(models.TrwIsp)]
        form = nas_forms.bas_update_form(isps)
        form.fill(self.db.query(models.TrwBas).get(bas_id))
        return self.render("base_form.html", form=form)

    def post(self):
        isps = [(t.isp_code, t.isp_name) for t in self.db.query(models.TrwIsp)]
        form = nas_forms.bas_update_form(isps)
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)
            
        bas = self.db.query(models.TrwBas).get(form.d.id)
        bas.bas_name = form.d.bas_name
        bas.dns_name = form.d.dns_name
        bas.time_type = form.d.time_type
        bas.vendor_id = form.d.vendor_id
        bas.portal_vendor = form.d.portal_vendor
        bas.bas_secret = form.d.bas_secret
        bas.coa_port = form.d.coa_port
        bas.ac_port = form.d.ac_port

        self.add_oplog(u'修改BAS信息:%s' % (bas.ip_addr))
        self.db.commit()

        self.redirect("/bas",permanent=False)

@permit.route(r"/bas/delete", u"接入设备删除", MenuRes, order=1.0003)
class DeleteHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        bas_id = self.get_argument("bas_id")
        self.db.query(models.TrwBas).filter_by(id=bas_id).delete()
        self.add_oplog(u'删除BAS信息:%s' % (bas_id))
        self.db.commit()
        self.redirect("/bas",permanent=False)






