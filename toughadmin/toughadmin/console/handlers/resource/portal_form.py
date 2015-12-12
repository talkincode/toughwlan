#!/usr/bin/env python
# coding=utf-8
from toughadmin.common import pyforms
from toughadmin.common.pyforms import dataform
from toughadmin.common.pyforms import rules
from toughadmin.common.pyforms.rules import button_style, input_style

portal_status = {0: u"正常", 1: u"未连接"}

portal_add_vform = dataform.Form(
    dataform.Item("ip_addr", rules.is_ip, description=u"portal地址"),
    dataform.Item("name", rules.len_of(0, 32), description=u"radius名称"),
    dataform.Item("secret", rules.len_of(1, 32), description=u"共享密钥"),
    dataform.Item("http_port", rules.is_number, description=u"认证端口"),
    dataform.Item("listen_port", rules.is_number, description=u"监听端口"),
    title="portal"
)
