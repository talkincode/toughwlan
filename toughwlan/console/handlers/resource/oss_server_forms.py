#!/usr/bin/env python
# coding=utf-8
from toughlib import btforms
from toughlib.btforms import rules
from toughlib.btforms.rules import button_style, input_style

serv_types = {0: u"备机", 1: u"主机"}

def oss_add_form():
    return btforms.Form(
        btforms.Textbox("name", rules.len_of(1, 32), description=u"OSS服务器名称",required="required", **input_style),
        btforms.Textbox("auth_url", rules.len_of(1, 255), description=u"OSS服务器认证地址",required="required", **input_style),
        btforms.Textbox("acct_url", rules.len_of(1, 255), description=u"OSS服务器记账地址",required="required", **input_style),
        btforms.Textbox("admin_url", rules.len_of(1, 255), description=u"OSS服务器管理地址",required="required", **input_style),
        btforms.Textbox("secret", rules.is_alphanum2(32, 32), description=u"共享秘钥", required="required",**input_style),
        btforms.Dropdown("serv_type", args=serv_types.items(),description=u"服务器类型(主|备)", required="required", **input_style),
        btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"增加OSS服务器信息",
        action="/oss/add",
    )

def oss_update_form():
    return btforms.Form(
        btforms.Hidden("id", description=u"编号"),
        btforms.Textbox("name", rules.len_of(1, 32), description=u"OSS服务器名称", required="required", **input_style),
        btforms.Textbox("auth_url", rules.len_of(1, 255), description=u"OSS服务器认证地址", required="required", **input_style),
        btforms.Textbox("acct_url", rules.len_of(1, 255), description=u"OSS服务器记账地址", required="required", **input_style),
        btforms.Textbox("admin_url", rules.len_of(1, 255), description=u"OSS服务器管理地址", required="required", **input_style),
        btforms.Textbox("secret", rules.is_alphanum2(32, 32), description=u"共享秘钥", required="required", **input_style),
        btforms.Dropdown("serv_type", args=serv_types.items(), description=u"服务器类型(主|备)", required="required", **input_style),
        btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"修改OSS服务器信息",
        action="/oss/update",
    )