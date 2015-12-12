#!/usr/bin/env python
# coding=utf-8
from toughadmin.common import pyforms
from toughadmin.common.pyforms import rules
from toughadmin.common.pyforms.rules import button_style, input_style


def tpl_add_form():
    return pyforms.Form(
        pyforms.Textbox("tpl_name", rules.len_of(4, 64), description=u"模版名称", required="required", **input_style),
        pyforms.Textarea("tpl_desc", description=u"模版描述", rows=4, **input_style),
        pyforms.Button("submit", type="submit", id="submit", html=u"<b>提交</b>", **button_style),
        title=u"增加模版",
        action="/template/add"
    )


def tpl_update_form():
    return pyforms.Form(
        pyforms.Hidden("id", description=u"编号"),
        pyforms.Textbox("tpl_name", rules.len_of(4, 64), description=u"模版名称", readonly="readonly", **input_style),
        pyforms.Textarea("tpl_desc", description=u"模版描述", rows=4, **input_style),
        pyforms.Button("submit", type="submit", html=u"<b>更新</b>", **button_style),
        title=u"修改模版",
        action="/template/update"
    )


tpl_attr_add_form = pyforms.Form(
    pyforms.Hidden("tpl_name", description=u"模版编号"),
    pyforms.Textbox("attr_name", rules.len_of(1, 255), description=u"属性名称", required="required",**input_style),
    pyforms.Textbox("attr_value", rules.len_of(1, 255), description=u"属性值", required="required", **input_style),
    pyforms.Textbox("attr_desc", rules.len_of(1, 255), description=u"属性描述", required="required", **input_style),
    pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"增加模版属性",
    action="/template/attr/add"
)

tpl_attr_update_form = pyforms.Form(
    pyforms.Hidden("id", description=u"编号"),
    pyforms.Hidden("tpl_name", description=u"模版编号"),
    pyforms.Textbox("attr_name", rules.len_of(1, 255), description=u"属性名称", readonly="readonly", **input_style),
    pyforms.Textbox("attr_value", rules.len_of(1, 255), description=u"属性值", required="required", **input_style),
    pyforms.Textbox("attr_desc", rules.len_of(1, 255), description=u"属性描述", required="required", **input_style),
    pyforms.Button("submit", type="submit", html=u"<b>更新</b>", **button_style),
    title=u"修改模版属性",
    action="/template/attr/update"
)

