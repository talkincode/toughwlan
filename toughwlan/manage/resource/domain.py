#!/usr/bin/env python
# coding:utf-8
import cyclone.web
from toughlib import utils
from toughwlan.admin.base import BaseHandler, MenuRes
from toughlib.permit import permit
from toughwlan import models
from toughwlan.admin.resource import domain_form


@permit.route(r"/domain", u"域信息管理", MenuRes, order=5.0000, is_menu=True)
class DomainHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.render("domain_list.html", page_data=self.get_page_data(self.db.query(models.TrwDomain)))

@permit.route(r"/domain/detail", u"域信息详情", MenuRes, order=5.0001)
class DomainDetailHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        domain_id = self.get_argument("domain_id")
        domain = self.db.query(models.TrwDomain).get(domain_id)
        attrs = self.db.query(models.TrwDomainAttr).filter_by(
            domain_code=domain.domain_code,isp_code=domain.isp_code)
        ssids = self.db.query(models.TrwSsid).filter_by(
            domain_code=domain.domain_code,isp_code=domain.isp_code)
        self.render("domain_detail.html", domain=domain, attrs=attrs,ssids=ssids)


@permit.route(r"/domain/add", u"域信息新增", MenuRes, order=5.0002)
class AddHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        tpls = [(t.tpl_name, t.tpl_desc) for t in self.db.query(models.TrwTemplate)]
        isps = [(t.isp_code, t.isp_name) for t in self.db.query(models.TrwIsp)]
        self.render("base_form.html", form=domain_form.domain_add_vform(tpls=tpls,isps=isps))

    @cyclone.web.authenticated
    def post(self):
        tpls = [(t.tpl_name, t.tpl_desc) for t in self.db.query(models.TrwTemplate)]
        isps = [(t.isp_code, t.isp_name) for t in self.db.query(models.TrwIsp)]
        form = domain_form.domain_add_vform(tpls=tpls, isps=isps)
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)
        if self.db.query(models.TrwDomain.id).filter_by(
            domain_code=form.d.domain_code,
            isp_code=form.d.isp_code).count() > 0:
            return self.render("base_form.html", form=form, msg=u"domain已经存在")
        domain = models.TrwDomain()
        domain.tpl_name = form.d.tpl_name
        domain.isp_code = form.d.isp_code
        domain.domain_code = form.d.domain_code
        domain.domain_desc = form.d.domain_desc
        self.db.add(domain)

        self.add_oplog(u'新增域信息:%s' % (form.d.domain_code))
        self.db.commit()
        self.redirect("/domain",permanent=False)

@permit.route(r"/domain/update", u"域信息修改", MenuRes, order=5.0003)
class UpdateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        domain_id = self.get_argument("domain_id")
        tpls = [(t.tpl_name, t.tpl_desc) for t in self.db.query(models.TrwTemplate)]
        isps = [(t.isp_code, t.isp_name) for t in self.db.query(models.TrwIsp)]
        form = domain_form.domain_update_vform(tpls=tpls,isps=isps)
        form.fill(self.db.query(models.TrwDomain).get(domain_id))
        return self.render("base_form.html", form=form)

    def post(self):
        tpls = [(t.tpl_name, t.tpl_desc) for t in self.db.query(models.TrwTemplate)]
        isps = [(t.isp_code, t.isp_name) for t in self.db.query(models.TrwIsp)]
        form = domain_form.domain_update_vform(tpls=tpls,isps=isps)
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)
        domain = self.db.query(models.TrwDomain).get(form.d.id)
        domain.tpl_name = form.d.tpl_name
        domain.domain_desc = form.d.domain_desc

        self.add_oplog( u'修改域信息:%s' % (domain.domain_code))
        self.db.commit()
        self.redirect("/domain",permanent=False)

@permit.route(r"/domain/delete", u"域信息删除", MenuRes, order=5.0004)
class DeleteHandler(BaseHandler):

    @cyclone.web.authenticated
    def post(self):
        domain_id = self.get_argument("domain_id")
        domain = self.db.query(models.TrwDomain).filter_by(id=domain_id).first()

        if self.db.query(models.TrwSsid).filter_by(
            domain_code=domain.domain_code,
            isp_code=domain.isp_code).count() > 0:
             return self.render_json(code=1, msg=u"此域下已关联SSID,不允许删除!")

        self.db.query(models.TrwDomain).filter_by(id=domain_id).delete()
        self.add_oplog(u'删除域信息:%s' % (domain_id))
        self.db.commit()
        return self.render_json(code=0, msg=u"删除域成功!")

@permit.route(r"/domain/attr/add", u"域属性新增", MenuRes, order=5.0005)
class DomainAttrAddHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        isp_code = self.get_argument("isp_code")
        domain_code = self.get_argument("domain_code")
        if self.db.query(models.TrwDomain).filter_by(
            domain_code=domain_code, isp_code=isp_code).count() == 0:
            return self.render_error(msg=u"域不存在")
        form = domain_form.domain_attr_add_form()
        form.domain_code.set_value(domain_code)
        form.isp_code.set_value(isp_code)
        self.render("base_form.html", form=form)

    @cyclone.web.authenticated
    def post(self):
        form = domain_form.domain_attr_add_form()
        if not form.validates(source=self.get_params()):
            return self.render("base_form,html", form=form)

        domain_attr = models.TrwDomainAttr()
        domain_attr.isp_code = form.d.isp_code
        domain_attr.domain_code = form.d.domain_code
        domain_attr.attr_name = form.d.attr_name
        domain_attr.attr_value = form.d.attr_value
        domain_attr.attr_desc = form.d.attr_desc
        self.db.add(domain_attr)

        self.db.commit()
        domain_id = self.db.query(models.TrwDomain.id).filter_by(
            domain_code=form.d.domain_code, isp_code=form.d.isp_code).scalar()
        self.redirect("/domain/detail?domain_id=%s" % domain_id)

@permit.route(r"/domain/attr/update", u"域属性修改", MenuRes, order=5.0006)
class DomainAttrUpdateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        attr_id = self.get_argument("attr_id")
        attr = self.db.query(models.TrwDomainAttr).get(attr_id)
        form = domain_form.domain_attr_update_form()
        form.fill(attr)
        self.render("base_form.html", form=form)

    @cyclone.web.authenticated
    def post(self, *args, **kwargs):
        form = domain_form.domain_attr_update_form()
        if not form.validates(source=self.get_params()):
            return self.render("base_form,html", form=form)

        domain_attr = self.db.query(models.TrwDomainAttr).get(form.d.id)
        domain_attr.attr_name = form.d.attr_name
        domain_attr.attr_value = form.d.attr_value
        domain_attr.attr_desc = form.d.attr_desc

        self.db.commit()
        domain_id = self.db.query(models.TrwDomain.id).filter_by(
            domain_code=form.d.domain_code,isp_code=form.d.isp_code).scalar()
        self.redirect("/domain/detail?domain_id=%s" % domain_id)

@permit.route(r"/domain/attr/delete", u"域属性删除", MenuRes, order=5.0007)
class DomainAttrDeleteHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        attr_id = self.get_argument("attr_id")
        attr = self.db.query(models.TrwDomainAttr).get(attr_id)
        self.db.query(models.TrwDomainAttr).filter_by(id=attr_id).delete()
        self.db.commit()
        domain_id = self.db.query(models.TrwDomain.id).filter_by(
            domain_code=attr.domain_code,isp_code=attr.isp_code).scalar()
        self.redirect("/domain/detail?domain_id=%s" % domain_id)



@permit.route(r"/domain/ssid/add", u"SSID信息新增", MenuRes, order=5.0008)
class AddHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        isp_code = self.get_argument("isp_code")
        domain_code = self.get_argument("domain_code")
        form=domain_form.ssid_add_form()
        form.isp_code.set_value(isp_code)
        form.domain_code.set_value(domain_code)
        self.render("base_form.html", form=form)

    @cyclone.web.authenticated
    def post(self):
        form = domain_form.ssid_add_form()
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)

        if self.db.query(models.TrwSsid.id).filter_by(
            ssid=form.d.ssid,
            isp_code=form.d.isp_code,
            domain_code=form.d.domain_code).count() > 0:
            return self.render("base_form.html", form=form, msg=u"ssid已经存在")

        mssid = models.TrwSsid()
        mssid.isp_code = form.d.isp_code
        mssid.domain_code = form.d.domain_code
        mssid.ssid = form.d.ssid
        mssid.ssid_desc = form.d.ssid_desc
        self.db.add(mssid)

        self.add_oplog(u'新增SSID信息:%s' % (mssid.ssid))
        self.db.commit()
        domain_id = self.db.query(models.TrwDomain.id).filter_by(
            domain_code=mssid.domain_code,isp_code=mssid.isp_code).scalar()
        self.redirect("/domain/detail?domain_id=%s" % domain_id)


@permit.route(r"/domain/ssid/delete", u"SSID信息删除", MenuRes, order=5.0009)
class DeleteHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        ssid_id = self.get_argument("ssid_id")
        mssid = self.db.query(models.TrwSsid).get(ssid_id)
        domain_id = self.db.query(models.TrwDomain.id).filter_by(
            domain_code=mssid.domain_code,isp_code=mssid.isp_code).scalar()
        self.db.query(models.TrwSsid).filter_by(id=ssid_id).delete()
        self.add_oplog(u'删除SSID信息:%s' % (ssid_id))
        self.db.commit()
        self.redirect("/domain/detail?domain_id=%s" % domain_id)





