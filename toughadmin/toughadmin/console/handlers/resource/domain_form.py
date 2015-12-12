#!/usr/bin/env python
# coding=utf-8
from toughadmin.common import pyforms
from toughadmin.common.pyforms import rules
from toughadmin.common.pyforms.rules import button_style, input_style


def domain_add_vform(tpls=[]):
    return pyforms.Form(
        pyforms.Dropdown("tpl_name", tpls, rules.not_null, description=u"模版", required="required", **input_style),
        pyforms.Textbox("domain_code", rules.is_alphanum2(2,16), description=u"域编码",required="required", **input_style),
        pyforms.Textbox("domain_desc", rules.not_null, description=u"域描述",required="required", **input_style),
        pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"增加域属性",
        action="/domain/add"
    )

def domain_update_vform(tpls=[]):
    return pyforms.Form(
        pyforms.Hidden("id", description=u"编号"),
        pyforms.Dropdown("tpl_name", tpls, rules.not_null, description=u"模版", required="required", **input_style),
        pyforms.Textbox("domain_code", rules.not_null, readonly="readonly", description=u"域编码",required="required", **input_style),
        pyforms.Textbox("domain_desc", rules.not_null, description=u"域描述",required="required", **input_style),
        pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"修改域属性",
        action="/domain/update"
    )


domain_attr_add_form = pyforms.Form(
    pyforms.Hidden("domain_code", description=u"域编码"),
    pyforms.Textbox("attr_name", rules.len_of(1, 255), description=u"属性名称", required="required", **input_style),
    pyforms.Textbox("attr_value", rules.len_of(1, 255), description=u"属性值", required="required", **input_style),
    pyforms.Textbox("attr_desc", rules.len_of(1, 255), description=u"属性描述", required="required", **input_style),
    pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"增加域属性",
    action="/domain/attr/add"
)

domain_attr_update_form = pyforms.Form(
    pyforms.Hidden("id", description=u"编号"),
    pyforms.Hidden("domain_code", description=u"域编码"),
    pyforms.Textbox("attr_name", rules.len_of(1, 255), description=u"属性名称", readonly="readonly", **input_style),
    pyforms.Textbox("attr_value", rules.len_of(1, 255), description=u"属性值", required="required", **input_style),
    pyforms.Textbox("attr_desc", rules.len_of(1, 255), description=u"属性描述", required="required", **input_style),
    pyforms.Button("submit", type="submit", html=u"<b>更新</b>", **button_style),
    title=u"修改域属性",
    action="/domain/attr/update"
)
