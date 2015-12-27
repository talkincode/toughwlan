#!/usr/bin/env python
# coding:utf-8
import cyclone.web
from toughwlan.console.handlers.base import BaseHandler, MenuRes
from toughlib.permit import permit
from toughwlan.console.handlers.resource import template_forms
from toughwlan.console import models

@permit.route(r"/template", u"认证模版管理", MenuRes, order=7.0000, is_menu=True)
class TemplateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        tpl_list = self.db.query(models.TraTemplate)
        self.render("template.html",tpl_list=tpl_list)


@permit.route(r"/template/add", u"模版新增", MenuRes, order=7.0001)
class TemplateAddHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        form = template_forms.tpl_add_form()
        self.render("base_form.html", form=form)

    @cyclone.web.authenticated
    def post(self, *args, **kwargs):
        form = template_forms.tpl_add_form()
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)

        tpl = models.TraTemplate()
        tpl.tpl_name = form.d.tpl_name
        tpl.tpl_desc = form.d.tpl_desc
        self.db.add(tpl)

        self.db.commit()
        self.redirect("/template")


@permit.route(r"/template/update", u"模版修改", MenuRes, order=7.0002)
class TemplateUpdateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        tpl_id = self.get_argument("tpl_id")
        form = template_forms.tpl_update_form()
        tpl = self.db.query(models.TraTemplate).get(tpl_id)
        form.fill(tpl)
        self.render("base_form.html",form=form)

    @cyclone.web.authenticated
    def post(self, *args, **kwargs):
        form = template_forms.tpl_update_form()
        if not form.validates(source=self.get_params()):
            return self.render("base_form,html", form=form)

        tpl = self.db.query(models.TraTemplate).get(form.d.id)
        if tpl:
            tpl.tpl_name = form.d.tpl_name
            tpl.tpl_desc = form.d.tpl_desc
            self.db.commit()

        self.redirect("/template")


@permit.route(r"/template/delete", u"模版删除", MenuRes, order=7.0003)
class TemplateDeleteHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self, *args, **kwargs):
        tpl_id = self.get_argument("tpl_id")
        self.db.query(models.TraTemplate).filter_by(id=tpl_id).delete()
        self.db.commit()
        self.redirect("/template")

@permit.route(r"/template/detail", u"模版详情", MenuRes, order=7.0004)
class TemplateDetailHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        tpl_id = self.get_argument("tpl_id")
        tpl = self.db.query(models.TraTemplate).get(tpl_id)
        attrs = self.db.query(models.TraTemplateAttr).filter_by(tpl_name=tpl.tpl_name)
        self.render("template_detail.html", tpl=tpl, attrs=attrs)

@permit.route(r"/template/attr/add", u"模版属性新增", MenuRes, order=7.0005)
class TemplateAttrAddHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        tpl_name = self.get_argument("tpl_name")
        if self.db.query(models.TraTemplate).filter_by(tpl_name=tpl_name).count() == 0:
            return self.render_error(msg=u"模版不存在")
        form = template_forms.tpl_attr_add_form()
        form.tpl_name.set_value(tpl_name)
        self.render("base_form.html",form=form)

    @cyclone.web.authenticated
    def post(self):
        form = template_forms.tpl_attr_add_form()
        if not form.validates(source=self.get_params()):
            return self.render("base_form,html", form=form)

        tpl_attr = models.TraTemplateAttr()
        tpl_attr.tpl_name = form.d.tpl_name
        tpl_attr.attr_name = form.d.attr_name
        tpl_attr.attr_value = form.d.attr_value
        tpl_attr.attr_desc = form.d.attr_desc
        self.db.add(tpl_attr)

        self.db.commit()
        tpl_id = self.db.query(models.TraTemplate.id).filter_by(tpl_name=form.d.tpl_name).scalar()
        self.redirect("/template/detail?tpl_id=%s"%tpl_id)

@permit.route(r"/template/attr/update", u"模版属性修改", MenuRes, order=7.0006)
class TemplateAttrUpdateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        attr_id = self.get_argument("attr_id")
        attr = self.db.query(models.TraTemplateAttr).get(attr_id)
        form = template_forms.tpl_attr_update_form()
        form.fill(attr)
        self.render("base_form.html", form=form)

    @cyclone.web.authenticated
    def post(self, *args, **kwargs):
        form = template_forms.tpl_attr_update_form()
        if not form.validates(source=self.get_params()):
            return self.render("base_form,html", form=form)

        tpl_attr = self.db.query(models.TraTemplateAttr).get(form.d.id)
        tpl_attr.attr_name = form.d.attr_name
        tpl_attr.attr_value = form.d.attr_value
        tpl_attr.attr_desc = form.d.attr_desc

        self.db.commit()
        tpl_id = self.db.query(models.TraTemplate.id).filter_by(tpl_name=form.d.tpl_name).scalar()
        self.redirect("/template/detail?tpl_id=%s" % tpl_id)

@permit.route(r"/template/attr/delete", u"模版属性删除", MenuRes, order=7.0007)
class TemplateAttrDeleteHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        attr_id = self.get_argument("attr_id")
        attr = self.db.query(models.TraTemplateAttr).get(attr_id)
        tpl_name = attr.tpl_name
        self.db.query(models.TraTemplateAttr).filter_by(id=attr_id).delete()

        self.db.commit()
        tpl_id = self.db.query(models.TraTemplate.id).filter_by(tpl_name=tpl_name).scalar()
        self.redirect("/template/detail?tpl_id=%s" % tpl_id)










