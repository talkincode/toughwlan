#!/usr/bin/env python
# coding=utf-8
from toughadmin.common.pyforms import dataform
from toughadmin.common.pyforms import rules

radius_status = {0: u"正常", 1: u"未连接"}

radius_add_vform = dataform.Form(
    dataform.Item("ip_addr", rules.is_ip, description=u"radius地址"),
    dataform.Item("name", rules.len_of(0, 32), description=u"radius名称"),
    dataform.Item("secret", rules.len_of(1, 32),description=u"radius密钥"),
    dataform.Item("auth_port", rules.is_number, description=u"认证端口"),
    dataform.Item("acct_port", rules.is_number, description=u"记账端口"),
    title="radius"
)