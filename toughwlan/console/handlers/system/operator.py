#!/usr/bin/env python
# coding:utf-8
from hashlib import md5
import cyclone.web
from toughlib import utils
from toughwlan.console.handlers.base import BaseHandler, MenuSys
from toughlib.permit import permit
from toughwlan.console import models
from toughwlan.console.handlers.system import operator_form
from toughwlan.console.handlers.system.operator_form import opr_status_dict


@permit.route(r"/operator", u"操作员管理", MenuSys, order=3.0000, is_menu=True)
class OperatorHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.render("operator_list.html",
                      operator_list=self.db.query(models.TraOperator),opr_status=opr_status_dict)


@permit.route(r"/operator/add", u"操作员新增", MenuSys, order=3.0001)
class AddHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.render("opr_form.html", form=operator_form.operator_add_form(),rules=[])

    @cyclone.web.authenticated
    def post(self):
        form = operator_form.operator_add_form()
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)
        if self.db.query(models.TraOperator.id).filter_by(operator_name=form.d.operator_name).count() > 0:
            return self.render("base_form.html", form=form, msg=u"操作员已经存在")
        operator = models.TraOperator()
        operator.operator_name = form.d.operator_name
        operator.operator_pass = md5(form.d.operator_pass.encode()).hexdigest()
        operator.operator_type = 1
        operator.operator_desc = form.d.operator_desc
        operator.operator_status = form.d.operator_status
        self.db.add(operator)

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.current_user.username
        ops_log.operate_ip = self.current_user.ipaddr
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'新增操作员信息:%s' % operator.operator_name
        self.db.add(ops_log)

        for path in self.get_arguments("rule_item"):
            item = permit.get_route(path)
            if not item: continue
            rule = models.TraOperatorRule()
            rule.operator_name = operator.operator_name
            rule.rule_name = item['name']
            rule.rule_path = item['path']
            rule.rule_category = item['category']
            self.db.add(rule)

        self.db.commit()

        for rule in self.db.query(models.TraOperatorRule).filter_by(operator_name=operator.operator_name):
            permit.bind_opr(rule.operator_name, rule.rule_path)

        self.redirect("/operator",permanent=False)

@permit.route(r"/operator/update", u"操作员修改", MenuSys, order=3.0002)
class UpdateHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        operator_id = self.get_argument("operator_id")
        opr = self.db.query(models.TraOperator).get(operator_id)
        form = operator_form.operator_update_form()
        form.fill(self.db.query(models.TraOperator).get(operator_id))
        form.operator_pass.set_value('')
        rules = self.db.query(models.TraOperatorRule.rule_path).filter_by(operator_name=opr.operator_name)
        rules = [r[0] for r in rules]
        return self.render("opr_form.html", form=form, rules=rules)

    def post(self):
        form = operator_form.operator_update_form()
        if not form.validates(source=self.get_params()):
            rules = self.db.query(models.TraOperatorRule.rule_path).filter_by(operator_name=form.d.operator_name)
            rules = [r[0] for r in rules]
            return self.render("base_form.html", form=form,rules=rules)
        operator = self.db.query(models.TraOperator).get(form.d.id)
        if form.d.operator_pass:
            operator.operator_pass = md5(form.d.operator_pass.encode()).hexdigest()
        operator.operator_desc = form.d.operator_desc
        operator.operator_status = form.d.operator_status

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'修改操作员%s信息' % operator.operator_name
        self.db.add(ops_log)

        # update rules
        self.db.query(models.TraOperatorRule).filter_by(operator_name=operator.operator_name).delete()

        for path in self.get_arguments("rule_item"):
            item = permit.get_route(path)
            if not item: continue
            rule = models.TraOperatorRule()
            rule.operator_name = operator.operator_name
            rule.rule_name = item['name']
            rule.rule_path = item['path']
            rule.rule_category = item['category']
            self.db.add(rule)

        permit.unbind_opr(operator.operator_name)

        self.db.commit()

        for rule in self.db.query(models.TraOperatorRule).filter_by(operator_name=operator.operator_name):
            permit.bind_opr(rule.operator_name, rule.rule_path)

        self.redirect("/operator",permanent=False)

@permit.route(r"/operator/delete", u"操作员删除", MenuSys, order=3.0003)
class DeleteHandler(BaseHandler):

    @cyclone.web.authenticated
    def get(self):
        operator_id = self.get_argument("operator_id")
        opr = self.db.query(models.TraOperator).get(operator_id)
        self.db.query(models.TraOperatorRule).filter_by(operator_name=opr.operator_name).delete()
        self.db.query(models.TraOperator).filter_by(id=operator_id).delete()

        ops_log = models.TraOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'删除操作员%s信息' % opr.operator_name
        self.db.add(ops_log)
        self.db.commit()
        self.redirect("/operator",permanent=False)




