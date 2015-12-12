#!/usr/bin/env python
#coding=utf-8
from toughadmin.common import pyforms
from toughadmin.common.pyforms import rules
from toughadmin.common.pyforms.rules import button_style, input_style

devtypes = {
    'PC': 'PC',
    'Phone': 'Phone',
    'Pad': 'Pad'
}

ostype_add_form = pyforms.Form(
    pyforms.Dropdown("dev_type", description=u"设备类型", args=devtypes.items(), required="required", **input_style),
    pyforms.Textbox("os_name", rules.len_of(1, 128), description=u"操作系统", required="required",**input_style),
    pyforms.Textbox("match_rule", rules.len_of(1, 128), description=u"匹配规则", required="required", **input_style),
    pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"设备类型新增",
    action="/ostype/add"
)

ostype_update_form = pyforms.Form(
    pyforms.Hidden("id", description=u"编号"),
    pyforms.Dropdown("dev_type", description=u"设备类型", args=devtypes.items(), required="required", **input_style),
    pyforms.Textbox("os_name", rules.len_of(1, 128), description=u"操作系统", required="required", **input_style),
    pyforms.Textbox("match_rule", rules.len_of(1, 128), description=u"匹配规则", required="required", **input_style),
    pyforms.Button("submit", type="submit", html=u"<b>更新</b>", **button_style),
    title=u"修改设备类型",
    action="/ostype/update"
)