#!/usr/bin/env python
# coding=utf-8
from toughlib import btforms
from toughlib.btforms import rules
from toughlib.btforms.rules import button_style, input_style


def tpl_add_form():
    return btforms.Form(
        btforms.Textbox("tpl_name", rules.len_of(4, 64), description=u"模版名称", required="required", **input_style),
        btforms.Textarea("tpl_desc", description=u"模版描述", rows=4, **input_style),
        btforms.Button("submit", type="submit", id="submit", html=u"<b>提交</b>", **button_style),
        title=u"增加模版",
        action="/template/add"
    )


def tpl_update_form():
    return btforms.Form(
        btforms.Hidden("id", description=u"编号"),
        btforms.Textbox("tpl_name", rules.len_of(4, 64), description=u"模版名称", readonly="readonly", **input_style),
        btforms.Textarea("tpl_desc", description=u"模版描述", rows=4, **input_style),
        btforms.Button("submit", type="submit", html=u"<b>更新</b>", **button_style),
        title=u"修改模版",
        action="/template/update"
    )


tpl_attr_add_form = btforms.Form(
    btforms.Hidden("tpl_name", description=u"模版编号"),
    btforms.Textbox("attr_name", rules.len_of(1, 255), description=u"属性名称", required="required",**input_style),
    btforms.Textbox("attr_value", rules.len_of(1, 255), description=u"属性值", required="required", **input_style),
    btforms.Textbox("attr_desc", rules.len_of(1, 255), description=u"属性描述", required="required", **input_style),
    btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"增加模版属性",
    action="/template/attr/add"
)

tpl_attr_update_form = btforms.Form(
    btforms.Hidden("id", description=u"编号"),
    btforms.Hidden("tpl_name", description=u"模版编号"),
    btforms.Textbox("attr_name", rules.len_of(1, 255), description=u"属性名称", readonly="readonly", **input_style),
    btforms.Textbox("attr_value", rules.len_of(1, 255), description=u"属性值", required="required", **input_style),
    btforms.Textbox("attr_desc", rules.len_of(1, 255), description=u"属性描述", required="required", **input_style),
    btforms.Button("submit", type="submit", html=u"<b>更新</b>", **button_style),
    title=u"修改模版属性",
    action="/template/attr/update"
)

