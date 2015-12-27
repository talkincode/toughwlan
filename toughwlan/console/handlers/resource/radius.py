#!/usr/bin/env python
# coding:utf-8

import cyclone.web
from toughlib import utils
from toughwlan.console.handlers.base import BaseHandler, MenuRes
from toughlib.permit import permit
from toughwlan.console.handlers.resource import radius_form
from toughwlan.console import models


@permit.route(r"/radius", u"Radius节点管理", MenuRes, order=2.0000, is_menu=True)
class RadiusHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        radius_list = self.db.query(models.TraRadius)
        self.render("radius.html",radius_list=radius_list)

@permit.route(r"/radius/detail", u"Radius节点详情", MenuRes, order=2.0001)
class RadiusDetailHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        radius_name = self.get_argument("radius_name")
        status = self.db.query(models.TraRadiusStatus).filter_by(radius_name=radius_name).first()
        self.render("radius_detail.html",status=status)

@permit.route(r"/radius/add", u"Radius节点新增", MenuRes, order=2.0003)
class AddHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.render("base_form.html", form=radius_form.radius_add_form())

    @cyclone.web.authenticated
    def post(self):
        form = radius_form.radius_add_form([])
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)

        if self.db.query(models.TraRadius.id).filter_by(ip_addr=form.d.ip_addr).count() > 0:
            return self.render("base_form.html", form=form, msg=u"ip地址已经存在")

        radius = models.TraRadius()
        radius.ip_addr = form.d.ip_addr
        radius.name = form.d.name
        radius.secret = form.d.secret
        radius.acct_port = form.d.acct_port
        radius.auth_port = form.d.auth_port
        radius.admin_url = form.d.admin_url
        radius.last_check = utils.get_currtime()
        self.db.add(radius)

        self.add_oplog(u'新增Radius信息:%s' % (radius.ip_addr))
        self.db.commit()
        self.redirect("/radius", permanent=False)


@permit.route(r"/radius/update", u"Radius节点修改", MenuRes, order=2.0004)
class UpdateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        radius_id = self.get_argument("radius_id")
        radius = self.db.query(models.TraRadius).get(radius_id)
        form = radius_form.radius_update_form()
        form.fill(radius)
        return self.render("base_form.html", form=form)

    def post(self):
        form = radius_form.radius_update_form([])
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)

        radius = self.db.query(models.TraRadius).get(form.d.id)
        radius.dns_name = form.d.dns_name
        radius.name = form.d.name
        radius.secret = form.d.secret
        radius.acct_port = form.d.acct_port
        radius.auth_port = form.d.auth_port
        radius.admin_url = form.d.admin_url

        self.add_oplog(u'修改Radius信息:%s' % (radius.ip_addr))
        self.db.commit()
        self.redirect("/radius", permanent=False)


@permit.route(r"/radius/delete", u"Radius节点删除", MenuRes, order=2.0005)
class RadiusDeleteHandler(BaseHandler):
    @cyclone.web.authenticated

    def get(self):
        radius_id = self.get_argument("radius_id")
        ip_addr = self.db.query(models.TraRadius.ip_addr).filter_by(id=radius_id).scalar()
        self.db.query(models.TraRadius).filter_by(id=radius_id).delete()
        self.add_oplog(u'删除radius信息:%s' % (ip_addr))
        self.db.commit()
        self.redirect("/radius",permanent=False)






