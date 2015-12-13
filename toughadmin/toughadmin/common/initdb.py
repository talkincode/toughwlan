#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0,os.path.split(__file__)[0])
sys.path.insert(0,os.path.abspath(os.path.pardir))
from toughadmin.common import utils
from toughadmin.console import models
from sqlalchemy.orm import scoped_session, sessionmaker
from hashlib import md5


def init_db(db):

    params = [
        ('system_name',u'管理系统名称',u'ToughWlan管理控制台'),
        ('is_debug',u'DEBUG模式',u'0'),
        ('smtp_server',u'SMTP服务器地址',u'smtp.mailgun.org'),
        ('smtp_user',u'SMTP用户名',u'service@toughradius.org'),
        ('smtp_pwd',u'SMTP密码',u'service2015'),
    ]

    for p in params:
        param = models.TraParam()
        param.param_name = p[0]
        param.param_desc = p[1]
        param.param_value = p[2]
        db.add(param)


    ostypes = [
        ["Phone", "ios", 'iPod'],
        ["Pad", "ios", 'iPad'],
        ["PC", "OSX", 'Intel Mac'],
        ["Phone", "ios", 'iPhone'],
        ["Phone", "symbian", 'symbian'],
        ["Phone", "android1", 'Android 1'],
        ["Phone", "android2", 'Android 2'],
        ["Phone", "android3", 'Android 3'],
        ["Phone", "android4", 'Android 4'],
        ["PC", "win2000", 'Windows NT 5.0'],
        ["PC", "winxp", 'Windows NT 5.1'],
        ["PC", "win2003", 'Windows NT 5.2'],
        ["PC", "winvista", 'Windows NT 6.0'],
        ["PC", "win7", 'Windows NT 6.1'],
        ["PC", "win8", 'Windows NT 6.2'],
        ["Phone", "winphone", 'Windows Phone'],
        ["Phone", "BlackBerry", 'BlackBerry'],
        ["PC", "linux", 'x11']
    ]


    for dev_type,os_name,match_rule in ostypes:
        otp = models.TraOSTypes()
        otp.os_name = os_name
        otp.dev_type = dev_type
        otp.match_rule = match_rule
        db.add(otp)


    opr = models.TraOperator()
    opr.id = 1
    opr.operator_name = u'admin'
    opr.operator_type = 0
    opr.operator_pass = md5('root').hexdigest()
    opr.operator_desc = 'admin'
    opr.operator_status = 0
    db.add(opr)

    domain = models.TraDomain()
    domain.id = 1
    domain.domain_code = 'default'
    domain.domain_desc = u'默认域'
    domain.tpl_name = 'default'
    db.add(domain)

    nas = models.TraBas()
    nas.ip_addr = "127.0.0.1"
    nas.bas_name = "local ac"
    nas.bas_secret = "testing123"
    nas.ac_port = 2000
    nas.coa_port = 3799
    nas.portal_vendor = "cmccv1"
    nas.time_type = 0
    nas.vendor_id = 3902
    db.add(nas)

    radius = models.TraRadius()
    radius.ip_addr = "127.0.0.1"
    radius.name = "local radius"
    radius.secret = "testing123"
    radius.acct_port = 1812
    radius.auth_port = 1813
    radius.status = 0
    radius.last_check = utils.get_currtime()
    db.add(radius)

    portal = models.TraPortal()
    portal.ip_addr = "127.0.0.1"
    portal.name = "local portal"
    portal.secret = "testing123"
    portal.http_port = 1812
    portal.listen_port = 1813
    portal.status = 0
    portal.last_check = utils.get_currtime()
    db.add(portal)

    ssid = models.TraSsid()
    ssid.domain_code = domain.domain_code
    ssid.ssid = 'default'
    ssid.ssid_desc = u'默认SSID'
    db.add(ssid)

    tpl = models.TraTemplate()
    tpl.id = 1
    tpl.tpl_name = 'default'
    tpl.tpl_desc = u'默认模版'
    db.add(tpl)

    tplattr1 = models.TraTemplateAttr()
    tplattr1.tpl_name = 'default'
    tplattr1.attr_name = 'page_title'
    tplattr1.attr_value = u'无线认证'
    tplattr1.attr_desc = u'页面标题'

    tplattr2 = models.TraTemplateAttr()
    tplattr2.tpl_name = 'default'
    tplattr2.attr_name = 'logo_url'
    tplattr2.attr_value = u'/static/img/plogin.png'
    tplattr2.attr_desc = u'logo地址'

    tplattr3 = models.TraTemplateAttr()
    tplattr3.tpl_name = 'default'
    tplattr3.attr_name = 'home_page'
    tplattr3.attr_value = u'http://www.baidu.com'
    tplattr3.attr_desc = u'认证成功重定向主页'

    db.add(tplattr1)
    db.add(tplattr2)
    db.add(tplattr3)


    db.commit()
    db.close()

def update(db_engine):
    print 'starting update database...'
    metadata = models.get_metadata(db_engine)
    metadata.drop_all(db_engine)
    metadata.create_all(db_engine)
    print 'update database done'
    db = scoped_session(sessionmaker(bind=db_engine, autocommit=False, autoflush=True))()
    init_db(db)


        