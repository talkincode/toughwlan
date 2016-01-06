#!/usr/bin/env python
# coding=utf-8
from toughlib import btforms
from toughlib.btforms import rules
from toughlib.btforms.rules import button_style, input_style

def isp_add_form():
    return btforms.Form(
        btforms.Textbox("isp_code", rules.len_of(4, 8), description=u"服务商编码", required="required", **input_style),
        btforms.Textbox("isp_name", rules.len_of(4, 64), description=u"服务商名称", required="required", **input_style),
        btforms.Textbox("isp_email", rules.len_of(0, 64), description=u"服务商Email", **input_style),
        btforms.Textbox("isp_phone", rules.len_of(0, 64), description=u"服务商电话", **input_style),
        btforms.Textbox("isp_idcard", rules.len_of(0, 32), description=u"服务商证件号码", **input_style),
        btforms.Textbox("isp_desc", description=u"服务商描述", **input_style),
        btforms.Button("submit", type="submit", id="submit", html=u"<b>提交</b>", **button_style),
        title=u"增加服务商",
        action="/isp/add"
    )


def isp_update_form():
    return btforms.Form(
        btforms.Textbox("isp_code", rules.len_of(4, 8), description=u"服务商编码", readonly="readonly", **input_style),
        btforms.Textbox("isp_name", rules.len_of(4, 64), description=u"服务商名称", **input_style),
        btforms.Textbox("isp_email", rules.len_of(0, 64), description=u"服务商Email", **input_style),
        btforms.Textbox("isp_phone", rules.len_of(0, 64), description=u"服务商电话", **input_style),
        btforms.Textbox("isp_idcard", rules.len_of(0, 32), description=u"服务商证件号码", **input_style),
        btforms.Textbox("isp_desc", description=u"服务商描述", **input_style),
        btforms.Button("submit", type="submit", html=u"<b>更新</b>", **button_style),
        title=u"修改服务商",
        action="/isp/update"
    )

