#!/usr/bin/env python
# coding=utf-8
from toughadmin.common import pyforms
from toughadmin.common.pyforms import rules
from toughadmin.common.pyforms.rules import button_style, input_style

boolean = {0: u"否", 1: u"是"}

def oss_add_form():
    return pyforms.Form(
        pyforms.Textbox("oss_server_ip", rules.is_ip, description=u"OSS服务器IP地址",required="required", **input_style),
        pyforms.Textbox("oss_auth_port", rules.is_number, description=u"OSS服务器认证端口",required="required", **input_style),
        pyforms.Textbox("oss_acct_port", rules.is_number, description=u"OSS服务器记账端口",required="required", **input_style),
        pyforms.Textbox("secret", rules.is_alphanum2(4, 32), description=u"共享秘钥", required="required",**input_style),
        pyforms.Dropdown("status", args=boolean.items(),description=u"状态,是否设置为主服务器", required="required",help=u'此项值选中会立即生效',**input_style),
        pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"增加OSS服务器信息",
        action="/oss/add",
    )

def oss_update_form():
    return pyforms.Form(
        pyforms.Hidden("id", description=u"编号"),
        pyforms.Textbox("oss_server_ip", rules.is_ip, description=u"OSS服务器IP地址",required="required", **input_style),
        pyforms.Textbox("oss_auth_port", rules.is_number, description=u"OSS服务器认证端口", required="required",**input_style),
        pyforms.Textbox("oss_acct_port", rules.is_number, description=u"OSS服务器记账端口", required="required",**input_style),
        pyforms.Textbox("secret", rules.is_alphanum2(4, 32), description=u"共享秘钥", required="required", **input_style),
        pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"修改OSS服务器信息",
        action="/oss/update",
    )