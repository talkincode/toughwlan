#!/usr/bin/env python
# coding:utf-8

import cyclone.web
from toughlib import utils
from toughwlan.admin.base import BaseHandler,MenuRes
from toughlib.permit import permit
from toughwlan import models
from toughwlan.admin.resource import isp_forms


@permit.route(r"/isp", u"服务商管理", MenuRes, order=2.1000, is_menu=True)
class IspHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.render("isp_list.html",isp_list=self.db.query(models.TrwIsp))


@permit.route(r"/isp/add", u"服务商新增", MenuRes, order=2.1001)
class AddHandler(BaseHandler):

    @cyclone.web.authenticated
    def get(self):
        self.render("base_form.html", form=isp_forms.isp_add_form())

    @cyclone.web.authenticated
    def post(self):
        form = isp_forms.isp_add_form()
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)

        if self.db.query(models.TrwIsp.id).filter_by(isp_code=form.d.isp_code).count() > 0:
            return self.render("base_form.html", form=form, msg=u"服务商编码已经存在")
            
        isp = models.TrwIsp()
        isp.isp_code = form.d.isp_code
        isp.isp_name = form.d.isp_name
        isp.isp_desc = form.d.isp_desc
        isp.isp_email = form.d.isp_email
        isp.isp_phone = form.d.isp_phone
        isp.isp_idcard = form.d.isp_idcard
        isp.user_total = 0
        isp.status = 0
        self.db.add(isp)

        self.add_oplog(u'新增ISP信息:%s' % ( isp.isp_code))
        self.db.commit()

        self.redirect("/isp",permanent=False)

@permit.route(r"/isp/update", u"服务商修改", MenuRes, order=2.10002)
class UpdateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        isp_code = self.get_argument("isp_code")
        form = isp_forms.isp_update_form()
        form.fill(self.db.query(models.TrwIsp).get(isp_code))
        return self.render("base_form.html", form=form)

    def post(self):
        form = isp_forms.isp_update_form()
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)
            
        isp = self.db.query(models.TrwIsp).get(form.d.isp_code)
        isp.isp_name = form.d.isp_name
        isp.isp_desc = form.d.isp_desc
        isp.isp_email = form.d.isp_email
        isp.isp_phone = form.d.isp_phone
        isp.isp_idcard = form.d.isp_idcard

        self.add_oplog(u'修改ISP信息:%s' % (isp.isp_code))
        self.db.commit()

        self.redirect("/isp",permanent=False)

@permit.route(r"/isp/delete", u"服务商删除", MenuRes, order=2.1003)
class DeleteHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        isp_code = self.get_argument("isp_code")
        self.db.query(models.TrwIsp).filter_by(isp_code=isp_code).delete()
        self.add_oplog(u'删除ISP信息:%s' % (isp_code))
        self.db.commit()
        self.redirect("/isp",permanent=False)






