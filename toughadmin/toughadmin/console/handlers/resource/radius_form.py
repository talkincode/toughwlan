#!/usr/bin/env python
# coding=utf-8
from toughadmin.common import pyforms
from toughadmin.common.pyforms import rules
from toughadmin.common.pyforms.rules import button_style, input_style

radius_add_form = pyforms.Form(
    pyforms.Textbox("ip_addr", rules.is_ip, description=u"radius地址", required="required", **input_style),
    pyforms.Textbox("name", rules.len_of(1, 32), description=u"radius名称", required="required", **input_style),
    pyforms.Textbox("secret", rules.len_of(1, 32),description=u"radius密钥", required="required", **input_style),
    pyforms.Textbox("auth_port", rules.is_number, description=u"认证端口", required="required", **input_style),
    pyforms.Textbox("acct_port", rules.is_number, description=u"记账端口", required="required", **input_style),
    pyforms.Textbox("admin_url", rules.len_of(1, 255), description=u"管理地址", required="required", **input_style),
    pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"新增radius",
    action="/radius/add"
)

radius_update_form = pyforms.Form(
    pyforms.Hidden("id", description=u"编号"),
    pyforms.Textbox("ip_addr", rules.is_ip, description=u"radius地址", required="required", **input_style),
    pyforms.Textbox("name", rules.len_of(1, 32), description=u"radius名称", required="required", **input_style),
    pyforms.Textbox("secret", rules.len_of(1, 32), description=u"radius密钥", required="required", **input_style),
    pyforms.Textbox("auth_port", rules.is_number, description=u"认证端口", required="required", **input_style),
    pyforms.Textbox("acct_port", rules.is_number, description=u"记账端口", required="required", **input_style),
    pyforms.Textbox("admin_url", rules.len_of(1, 255), description=u"管理地址", required="required", **input_style),
    pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"修改radius",
    action="/radius/update"
)


