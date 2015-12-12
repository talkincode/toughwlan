#!/usr/bin/env python
# coding=utf-8
from toughadmin.common import pyforms
from toughadmin.common.pyforms import rules
from toughadmin.common.pyforms.rules import button_style, input_style

def ssid_add_form(domains=[]):
    return pyforms.Form(
        pyforms.Dropdown("domain_code",domains,rules.not_null, description=u"域编码", required="required", **input_style),
        pyforms.Textbox("ssid", rules.not_null, description=u"ssid",required="required", **input_style),
        pyforms.Textbox("ssid_desc", rules.not_null, description=u"ssid描述",required="required", **input_style),
        pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"增加SSID属性",
        action="/ssid/add",
    )

def ssid_update_form(domains=[]):
    return pyforms.Form(
        pyforms.Hidden("id", description=u"编号"),
        pyforms.Dropdown("domain_code", args=domains, description=u"域编码", required="required", **input_style),
        pyforms.Textbox("ssid", rules.not_null,description=u"ssid",required="required",readonly="readonly", **input_style),
        pyforms.Textbox("ssid_desc", rules.not_null, description=u"ssid描述",required="required", **input_style),
        pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"修改SSID属性",
        action="/ssid/update",
    )