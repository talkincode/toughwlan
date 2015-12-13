#!/usr/bin/env python
# coding=utf-8
from toughadmin.common import pyforms
from toughadmin.common.pyforms import rules
from toughadmin.common.pyforms.rules import button_style, input_style

portal_status = {0: u"正常", 1: u"未连接"}

portal_add_form = pyforms.Form(
    pyforms.Textbox("ip_addr", rules.is_ip, description=u"portal地址", required="required", **input_style),
    pyforms.Textbox("name", rules.len_of(0, 32), description=u"portal名称", required="required", **input_style),
    pyforms.Textbox("secret", rules.len_of(1, 32), description=u"共享密钥", required="required", **input_style),
    pyforms.Textbox("http_port", rules.is_number, description=u"认证端口", required="required", **input_style),
    pyforms.Textbox("listen_port", rules.is_number, description=u"监听端口", required="required", **input_style),
    pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"新增portal",
    action="/portal/add"
)

portal_update_form = pyforms.Form(
    pyforms.Textbox("ip_addr", rules.is_ip, description=u"portal地址", required="required", **input_style),
    pyforms.Textbox("name", rules.len_of(0, 32), description=u"portal名称", required="required", **input_style),
    pyforms.Textbox("secret", rules.len_of(1, 32), description=u"共享密钥", required="required", **input_style),
    pyforms.Textbox("http_port", rules.is_number, description=u"认证端口", required="required", **input_style),
    pyforms.Textbox("listen_port", rules.is_number, description=u"监听端口", required="required", **input_style),
    pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"修改portal",
    action="/portal/update"
)
