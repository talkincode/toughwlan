#!/usr/bin/env python
#coding=utf-8
from toughlib import btforms
from toughlib.btforms import rules
from toughlib.btforms.rules import button_style, input_style

devtypes = {
    'PC': 'PC',
    'Phone': 'Phone',
    'Pad': 'Pad'
}

ostype_add_form = btforms.Form(
    btforms.Dropdown("dev_type", description=u"设备类型", args=devtypes.items(), required="required", **input_style),
    btforms.Textbox("os_name", rules.len_of(1, 128), description=u"操作系统", required="required",**input_style),
    btforms.Textbox("match_rule", rules.len_of(1, 128), description=u"匹配规则", required="required", **input_style),
    btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"设备类型新增",
    action="/ostype/add"
)

ostype_update_form = btforms.Form(
    btforms.Hidden("id", description=u"编号"),
    btforms.Dropdown("dev_type", description=u"设备类型", args=devtypes.items(), required="required", **input_style),
    btforms.Textbox("os_name", rules.len_of(1, 128), description=u"操作系统", required="required", **input_style),
    btforms.Textbox("match_rule", rules.len_of(1, 128), description=u"匹配规则", required="required", **input_style),
    btforms.Button("submit", type="submit", html=u"<b>更新</b>", **button_style),
    title=u"修改设备类型",
    action="/ostype/update"
)