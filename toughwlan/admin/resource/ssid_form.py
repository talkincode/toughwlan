#!/usr/bin/env python
# coding=utf-8
from toughlib import btforms
from toughlib.btforms import rules
from toughlib.btforms.rules import button_style, input_style

def ssid_add_form(domains=[]):
    return btforms.Form(
        btforms.Dropdown("domain_code",domains,rules.not_null, description=u"域编码", required="required", **input_style),
        btforms.Textbox("ssid", rules.not_null, description=u"ssid",required="required", **input_style),
        btforms.Textbox("ssid_desc", rules.not_null, description=u"ssid描述",required="required", **input_style),
        btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"增加SSID属性",
        action="/ssid/add",
    )

def ssid_update_form(domains=[]):
    return btforms.Form(
        btforms.Hidden("id", description=u"编号"),
        btforms.Dropdown("domain_code", args=domains, description=u"域编码", required="required", **input_style),
        btforms.Textbox("ssid", rules.not_null,description=u"ssid",required="required",readonly="readonly", **input_style),
        btforms.Textbox("ssid_desc", rules.not_null, description=u"ssid描述",required="required", **input_style),
        btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"修改SSID属性",
        action="/ssid/update",
    )