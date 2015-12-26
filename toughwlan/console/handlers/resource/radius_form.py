#!/usr/bin/env python
# coding=utf-8
from toughlib import btforms
from toughlib.btforms import rules
from toughlib.btforms.rules import button_style, input_style

radius_add_form = btforms.Form(
    btforms.Textbox("ip_addr", rules.is_ip, description=u"radius地址", required="required", **input_style),
    btforms.Textbox("name", rules.len_of(1, 32), description=u"radius名称", required="required", **input_style),
    btforms.Textbox("secret", rules.len_of(1, 32),description=u"radius密钥", required="required", **input_style),
    btforms.Textbox("auth_port", rules.is_number, description=u"认证端口", required="required", **input_style),
    btforms.Textbox("acct_port", rules.is_number, description=u"记账端口", required="required", **input_style),
    btforms.Textbox("admin_url", rules.len_of(1, 255), description=u"管理地址", required="required", **input_style),
    btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"新增radius",
    action="/radius/add"
)

radius_update_form = btforms.Form(
    btforms.Hidden("id", description=u"编号"),
    btforms.Textbox("ip_addr", rules.is_ip, description=u"radius地址", required="required", **input_style),
    btforms.Textbox("name", rules.len_of(1, 32), description=u"radius名称", required="required", **input_style),
    btforms.Textbox("secret", rules.len_of(1, 32), description=u"radius密钥", required="required", **input_style),
    btforms.Textbox("auth_port", rules.is_number, description=u"认证端口", required="required", **input_style),
    btforms.Textbox("acct_port", rules.is_number, description=u"记账端口", required="required", **input_style),
    btforms.Textbox("admin_url", rules.len_of(1, 255), description=u"管理地址", required="required", **input_style),
    btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"修改radius",
    action="/radius/update"
)


