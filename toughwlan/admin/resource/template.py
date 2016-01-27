#!/usr/bin/env python
# coding:utf-8
import cyclone.web
from toughwlan.admin.base import BaseHandler, MenuRes
from toughlib.permit import permit
from toughwlan.admin.resource import template_forms
from toughwlan import models

@permit.route(r"/template", u"认证模版管理", MenuRes, order=7.0000, is_menu=True)
class TemplateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        tpl_list = self.db.query(models.TrwTemplate)
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

        tpl = models.TrwTemplate()
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
        tpl = self.db.query(models.TrwTemplate).get(tpl_id)
        form.fill(tpl)
        self.render("base_form.html",form=form)

    @cyclone.web.authenticated
    def post(self, *args, **kwargs):
        form = template_forms.tpl_update_form()
        if not form.validates(source=self.get_params()):
            return self.render("base_form,html", form=form)

        tpl = self.db.query(models.TrwTemplate).get(form.d.id)
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
        self.db.query(models.TrwTemplate).filter_by(id=tpl_id).delete()
        self.db.commit()
        self.redirect("/template")












