#!/usr/bin/env python
# coding=utf-8
from toughlib import btforms
from toughlib.btforms import rules
from toughlib.btforms.rules import button_style, input_style

portal_status = {0: u"正常", 1: u"未连接"}

portal_add_form = btforms.Form(
    btforms.Textbox("ip_addr", rules.is_ip, description=u"portal地址", required="required", **input_style),
    btforms.Textbox("name", rules.len_of(1, 32), description=u"portal名称", required="required", **input_style),
    btforms.Textbox("listen_port", rules.is_number, description=u"监听端口", required="required", **input_style),
    btforms.Textbox("secret", rules.len_of(1, 32), description=u"共享密钥", required="required", **input_style),
    btforms.Textbox("auth_url", rules.len_of(1, 255), description=u"认证地址", required="required", **input_style),
    btforms.Textbox("admin_url", rules.len_of(1, 255), description=u"管理地址", required="required", **input_style),
    btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"新增portal",
    action="/portal/add"
)

portal_update_form = btforms.Form(
    btforms.Hidden("id", description=u"编号"),
    btforms.Textbox("ip_addr", rules.is_ip, description=u"portal地址", required="required", **input_style),
    btforms.Textbox("name", rules.len_of(1, 32), description=u"portal名称", required="required", **input_style),
    btforms.Textbox("listen_port", rules.is_number, description=u"监听端口", required="required", **input_style),
    btforms.Textbox("secret", rules.len_of(1, 32), description=u"共享密钥", required="required", **input_style),
    btforms.Textbox("auth_url", rules.len_of(1, 255), description=u"认证地址", required="required", **input_style),
    btforms.Textbox("admin_url", rules.len_of(1, 255), description=u"管理地址", required="required", **input_style),
    btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"修改portal",
    action="/portal/update"
)
