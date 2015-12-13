#!/usr/bin/env python
#coding=utf-8
from toughadmin.common import pyforms
from toughadmin.common.pyforms import rules
from toughadmin.common.pyforms.rules import button_style, input_style

boolean = {0: u"否", 1: u"是"}
timetype = {0: u"标准时区,北京时间", 1: u"时区和时间同区"}
portaltype = {'cmccv1': "CMCC V1", 'cmccv2': "CMCC V2", 'huwweiv1': "HUAWEI V1", 'huwweiv2': "HUAWEI V2" }

bastype = {
    '0'    : u'标准',
    # '9': u'思科',
    # '3041': u'阿尔卡特',
    '2352': u'爱立信',
    '2011': u'华为',
    '25506': u'H3C',
    '3902': u'中兴',
    '10055': u'爱快',
    '14988': u'RouterOS'
}

bas_add_form = pyforms.Form(
    pyforms.Textbox("ip_addr", rules.is_ip, description=u"设备地址", required="required", **input_style),
    pyforms.Textbox("bas_name", rules.len_of(2, 64), description=u"设备名称", required="required", **input_style),
    pyforms.Textbox("bas_secret", rules.is_alphanum2(4, 32), description=u"共享秘钥", required="required", **input_style),
    pyforms.Dropdown("vendor_id", description=u"设备类型", args=bastype.items(), required="required", **input_style),
    pyforms.Dropdown("portal_vendor", description=u"portal协议", args=portaltype.items(), required="required", **input_style),
    pyforms.Dropdown("time_type", description=u"时区类型", args=timetype.items(), required="required", **input_style),
    pyforms.Textbox("ac_port", rules.is_number, description=u"AC端口", default=2000, required="required",**input_style),
    pyforms.Textbox("coa_port", rules.is_number, description=u"CoA端口", default=3799, required="required",**input_style),
    pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"增加接入设备",
    action="/bas/add"
)

bas_update_form = pyforms.Form(
    pyforms.Hidden("id", description=u"编号"),
    pyforms.Textbox("ip_addr", rules.is_ip, description=u"设备地址", required="required", readonly="readonly", **input_style),
    pyforms.Textbox("bas_name", rules.len_of(2, 64), description=u"设备名称", required="required", **input_style),
    pyforms.Textbox("bas_secret", rules.is_alphanum2(4, 32), description=u"共享秘钥", required="required", **input_style),
    pyforms.Dropdown("vendor_id", description=u"设备类型", args=bastype.items(), required="required", **input_style),
    pyforms.Dropdown("portal_vendor", description=u"portal协议", args=portaltype.items(), required="required",**input_style),
    pyforms.Dropdown("time_type", description=u"时区类型", args=timetype.items(), required="required", **input_style),
    pyforms.Textbox("ac_port", rules.is_number, description=u"AC端口", default=2000, required="required",**input_style),
    pyforms.Textbox("coa_port", rules.is_number, description=u"CoA端口", default=3799, required="required",**input_style),
    pyforms.Button("submit", type="submit", html=u"<b>更新</b>", **button_style),
    title=u"修改接入设备",
    action="/bas/update"
)