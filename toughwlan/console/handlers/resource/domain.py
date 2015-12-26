#!/usr/bin/env python
# coding:utf-8

import cyclone.auth
import cyclone.escape
import cyclone.web

from toughlib import utils
from toughwlan.console.handlers.base import BaseHandler, MenuRes
from toughlib.permit import permit
from toughwlan.console import models
from toughwlan.console.handlers.resource import domain_form


@permit.route(r"/domain", u"域信息管理", MenuRes, order=5.0000, is_menu=True)
class DomainHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.render("domain_list.html", page_data=self.get_page_data(self.db.query(models.TraDomain)))

@permit.route(r"/domain/detail", u"域信息详情", MenuRes, order=5.0001)
class DomainDetailHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        domain_id = self.get_argument("domain_id")
        domain = self.db.query(models.TraDomain).get(domain_id)
        attrs = self.db.query(models.TraDomainAttr).filter_by(domain_code=domain.domain_code)
        self.render("domain_detail.html", domain=domain, attrs=attrs)


@permit.route(r"/domain/add", u"域信息新增", MenuRes, order=5.0002)
class AddHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        tpls = [(t.tpl_name, t.tpl_desc) for t in self.db.query(models.TraTemplate)]
        self.render("base_form.html", form=domain_form.domain_add_vform(tpls=tpls))

    @cyclone.web.authenticated
    def post(self):
        tpls = [(t.tpl_name, t.tpl_desc) for t in self.db.query(models.TraTemplate)]
        form = domain_form.domain_add_vform(tpls=tpls)
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)
        if self.db.query(models.TraDomain.id).filter_by(domain_code=form.d.domain_code).count() > 0:
            return self.render("base_form.html", form=form, msg=u"domain已经存在")
        domain = models.TraDomain()
        domain.tpl_name = form.d.tpl_name
        domain.domain_code = form.d.domain_code
        domain.domain_desc = form.d.domain_desc
        self.db.add(domain)

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.current_user.username
        ops_log.operate_ip = self.current_user.ipaddr
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)新增域信息:%s' % (ops_log.operator_name, form.d.domain_code)
        self.db.add(ops_log)

        self.db.commit()
        self.redirect("/domain",permanent=False)

@permit.route(r"/domain/update", u"域信息修改", MenuRes, order=5.0003)
class UpdateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        domain_id = self.get_argument("domain_id")
        tpls = [(t.tpl_name, t.tpl_desc) for t in self.db.query(models.TraTemplate)]
        form = domain_form.domain_update_vform(tpls=tpls)
        form.fill(self.db.query(models.TraDomain).get(domain_id))
        return self.render("base_form.html", form=form)

    def post(self):
        tpls = [(t.tpl_name, t.tpl_desc) for t in self.db.query(models.TraTemplate)]
        form = domain_form.domain_update_vform(tpls=tpls)
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)
        domain = self.db.query(models.TraDomain).get(form.d.id)
        domain.tpl_name = form.d.tpl_name
        domain.domain_desc = form.d.domain_desc

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)修改域信息:%s' % (ops_log.operator_name, domain.domain_code)
        self.db.add(ops_log)

        self.db.commit()
        self.redirect("/domain",permanent=False)

@permit.route(r"/domain/delete", u"域信息删除", MenuRes, order=5.0004)
class DeleteHandler(BaseHandler):

    @cyclone.web.authenticated
    def post(self):
        domain_id = self.get_argument("domain_id")
        domain_code = self.db.query(models.TraDomain.domain_code).filter_by(id=domain_id).scalar()

        if self.db.query(models.TraSsid).filter_by(domain_code=domain_code).count() > 0:
             return self.render_json(code=1, msg=u"此域下已关联SSID,不允许删除!")

        self.db.query(models.TraDomain).filter_by(id=domain_id).delete()

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)删除域信息:%s' % (ops_log.operator_name, domain_id)
        self.db.add(ops_log)

        self.db.commit()
        return self.render_json(code=0, msg=u"删除域成功!")

@permit.route(r"/domain/attr/add", u"域属性新增", MenuRes, order=5.0005)
class DomainAttrAddHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        domain_code = self.get_argument("domain_code")
        if self.db.query(models.TraDomain).filter_by(domain_code=domain_code).count() == 0:
            return self.render_error(msg=u"域不存在")
        form = domain_form.domain_attr_add_form()
        form.domain_code.set_value(domain_code)
        self.render("base_form.html", form=form)

    @cyclone.web.authenticated
    def post(self):
        form = domain_form.domain_attr_add_form()
        if not form.validates(source=self.get_params()):
            return self.render("base_form,html", form=form)

        domain_attr = models.TraDomainAttr()
        domain_attr.domain_code = form.d.domain_code
        domain_attr.attr_name = form.d.attr_name
        domain_attr.attr_value = form.d.attr_value
        domain_attr.attr_desc = form.d.attr_desc
        self.db.add(domain_attr)

        self.db.commit()
        domain_id = self.db.query(models.TraDomain.id).filter_by(domain_code=form.d.domain_code).scalar()
        self.redirect("/domain/detail?domain_id=%s" % domain_id)

@permit.route(r"/domain/attr/update", u"域属性修改", MenuRes, order=5.0006)
class DomainAttrUpdateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        attr_id = self.get_argument("attr_id")
        attr = self.db.query(models.TraDomainAttr).get(attr_id)
        form = domain_form.domain_attr_update_form()
        form.fill(attr)
        self.render("base_form.html", form=form)

    @cyclone.web.authenticated
    def post(self, *args, **kwargs):
        form = domain_form.domain_attr_update_form()
        if not form.validates(source=self.get_params()):
            return self.render("base_form,html", form=form)

        domain_attr = self.db.query(models.TraDomainAttr).get(form.d.id)
        domain_attr.attr_name = form.d.attr_name
        domain_attr.attr_value = form.d.attr_value
        domain_attr.attr_desc = form.d.attr_desc

        self.db.commit()
        domain_id = self.db.query(models.TraDomain.id).filter_by(domain_code=form.d.domain_code).scalar()
        self.redirect("/domain/detail?domain_id=%s" % domain_id)

@permit.route(r"/domain/attr/delete", u"域属性删除", MenuRes, order=5.0007)
class DomainAttrDeleteHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        attr_id = self.get_argument("attr_id")
        attr = self.db.query(models.TraDomainAttr).get(attr_id)
        domain_code = attr.domain_code
        self.db.query(models.TraDomainAttr).filter_by(id=attr_id).delete()
        self.db.commit()
        domain_id = self.db.query(models.TraDomain.id).filter_by(domain_code=domain_code).scalar()
        self.redirect("/domain/detail?domain_id=%s" % domain_id)











