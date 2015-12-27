#!/usr/bin/env python
#coding:utf-8
import warnings

import sqlalchemy

warnings.simplefilter('ignore', sqlalchemy.exc.SAWarning)
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


def get_metadata(db_engine):
    global DeclarativeBase
    metadata = DeclarativeBase.metadata
    metadata.bind = db_engine
    return metadata


class SystemSession(DeclarativeBase):
    """session表"""
    __tablename__ = 'system_session'

    __table_args__ = {
        'mysql_engine' : 'MEMORY'
    }

    key = Column(u'_key', Unicode(length=512), primary_key=True, nullable=False,doc=u"session key")
    value = Column(u'_value', Unicode(length=2048), nullable=False,doc=u"session value")
    time = Column(u'_time', INTEGER(), nullable=False,doc=u"session timeout")

class SystemCache(DeclarativeBase):
    """cache表"""
    __tablename__ = 'system_cache'

    __table_args__ = {
        'mysql_engine' : 'MEMORY'
    }

    key = Column(u'_key', Unicode(length=512), primary_key=True, nullable=False,doc=u"cache key")
    value = Column(u'_value', Unicode(length=4096), nullable=False,doc=u"cache value")
    time = Column(u'_time', INTEGER(), nullable=False,doc=u"cache timeout")



class TraOperator(DeclarativeBase):
    """操作员表 操作员类型 0 系统管理员 1 普通操作员"""
    __tablename__ = 'tra_operator'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"操作员id")
    operator_type = Column('operator_type', INTEGER(), nullable=False,doc=u"操作员类型")
    operator_name = Column(u'operator_name', Unicode(32), nullable=False,doc=u"操作员名称")
    operator_pass = Column(u'operator_pass', Unicode(length=128), nullable=False,doc=u"操作员密码")
    operator_status = Column(u'operator_status', INTEGER(), nullable=False,doc=u"操作员状态,0/1")
    operator_desc = Column(u'operator_desc', Unicode(255), nullable=False,doc=u"操作员描述")

class TraOperatorRule(DeclarativeBase):
    """操作员权限表"""
    __tablename__ = 'tra_operator_rule'

    __table_args__ = {}
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"权限id")
    operator_name = Column(u'operator_name', Unicode(32), nullable=False,doc=u"操作员名称")
    rule_path = Column(u'rule_path', Unicode(128), nullable=False,doc=u"权限URL")
    rule_name = Column(u'rule_name', Unicode(128), nullable=False,doc=u"权限名称")
    rule_category = Column(u'rule_category', Unicode(128), nullable=False,doc=u"权限分类")


class TraParam(DeclarativeBase):
    """系统参数表  """
    __tablename__ = 'tra_param'

    __table_args__ = {}

    #column definitions
    param_name = Column(u'param_name', Unicode(length=64), primary_key=True, nullable=False,doc=u"参数名")
    param_value = Column(u'param_value', Unicode(length=1024), nullable=False,doc=u"参数值")
    param_desc = Column(u'param_desc', Unicode(length=255),doc=u"参数描述")

    #relation definitions

class TraBas(DeclarativeBase):
    """BAS设备表 """
    __tablename__ = 'tra_bas'

    __table_args__ = {}

    # column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, doc=u"设备id")
    ip_addr = Column(u'ip_addr', Unicode(length=15), nullable=True, doc=u"IP地址")
    dns_name = Column(u'dns_name', Unicode(length=128), nullable=True, doc=u"DNS名称")
    bas_name = Column(u'bas_name', Unicode(length=64), nullable=False, doc=u"bas名称")
    bas_secret = Column(u'bas_secret', Unicode(length=64), nullable=False, doc=u"共享密钥")
    vendor_id = Column(u'vendor_id', SMALLINT(), nullable=False, doc=u"bas类型")
    portal_vendor = Column(u'portal_vendor', Unicode(length=64), nullable=False, doc=u"portal协议")
    time_type = Column(u'time_type', SMALLINT(), nullable=False, doc=u"时区类型")
    ac_port = Column(u'ac_port', INTEGER(), nullable=False, doc=u"AC端口")
    coa_port = Column(u'coa_port', INTEGER(), nullable=False, doc=u"CoA端口")

    # relation definiti



class TraDomain(DeclarativeBase):
    """域属性表 """
    __tablename__ = 'tra_domain'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"id")
    domain_code = Column(u'domain_code', Unicode(length=16), nullable=False, index=True, doc=u"域编码")
    tpl_name = Column(u'tpl_name', Unicode(length=64), nullable=False, doc=u"模版名称")
    domain_desc = Column(u'domain_desc', Unicode(length=64), nullable=False, doc=u"域描述")

class TraDomainAttr(DeclarativeBase):
    """portal模版属性 """
    __tablename__ = 'tra_domain_attr'

    __table_args__ = {}

    # column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, doc=u"模版属性id")
    domain_code = Column(u'domain_code', Unicode(length=16), nullable=False, doc=u"域编码")
    attr_name = Column(u'attr_name', Unicode(length=128), nullable=False, doc=u"模版名")
    attr_value = Column(u'attr_value', Unicode(length=1024), nullable=False, doc=u"属性值")
    attr_desc = Column(u'attr__desc', Unicode(length=255), doc=u"属性描述")

class TraSsid(DeclarativeBase):
    """SSID信息表 """
    __tablename__ = 'tra_ssid'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"id")
    domain_code = Column(u'domain_code', Unicode(length=16), nullable=False,doc=u"域编码")
    ssid = Column(u'ssid', Unicode(length=16), nullable=False, index=True, doc=u"ssid")
    ssid_desc = Column(u'ssid_desc', Unicode(length=64), nullable=False, doc=u"ssid描述")


class TraRadius(DeclarativeBase):
    """radius节点表 """
    __tablename__ = 'tra_radius'

    __table_args__ = {}

    # column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, doc=u"设备id")
    ip_addr = Column(u'ip_addr', Unicode(length=15), nullable=False, doc=u"IP地址")
    name = Column(u'name', Unicode(length=64), nullable=False, doc=u"radius名称")
    secret = Column(u'secret', Unicode(length=64), nullable=False, doc=u"共享密钥")
    auth_port = Column(u'auth_port', INTEGER(), nullable=False, doc=u"认证端口")
    acct_port = Column(u'acct_port', INTEGER(), nullable=False, doc=u"记账端口")
    admin_url = Column(u'admin_url', Unicode(length=255), nullable=False, doc=u"管理地址")
    last_check = Column(u'last_check', Unicode(length=19), nullable=True, doc=u"最后检测")

class TraRadiusStatus(DeclarativeBase):
    """radius状态信息表 """
    __tablename__ = 'tra_radius_status'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"id")
    ip_addr = Column(u'ip_addr', Unicode(length=16), nullable=False,doc=u"radius地址")
    stat_time = Column(u'stat_time', Unicode(length=16), nullable=False, doc=u"统计时间")
    auth_all = Column(u'auth_all', INTEGER(), nullable=False, doc=u"认证总数")
    auth_accept = Column(u'auth_accept', INTEGER(), nullable=False, doc=u"认证成功数")
    auth_reject = Column(u'auth_reject', INTEGER(), nullable=False, doc=u"认证拒绝数")
    acct_all = Column(u'acct_all', INTEGER(), nullable=False, doc=u"记账总数")
    acct_start = Column(u'acct_start', INTEGER(), nullable=False, doc=u"记账开始数")
    acct_stop = Column(u'acct_stop', INTEGER(), nullable=False, doc=u"记账结束数")
    acct_update = Column(u'acct_update', INTEGER(), nullable=False, doc=u"记账更新数")
    acct_on = Column(u'acct_on', INTEGER(), nullable=False, doc=u"记账上线数")
    acct_off = Column(u'acct_off', INTEGER(), nullable=False, doc=u"记账下线数")


class TraTemplate(DeclarativeBase):
    """portal模版 """
    __tablename__ = 'tra_template'

    __table_args__ = {}

    # column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, doc=u"模版id")
    tpl_name = Column(u'tpl_name', Unicode(length=64), nullable=False, doc=u"模版名称")
    tpl_desc = Column(u'tpl_desc', Unicode(length=512), nullable=False, doc=u"模版描述")


class TraTemplateAttr(DeclarativeBase):
    """portal模版属性 """
    __tablename__ = 'tra_template_attr'

    __table_args__ = {}

    # column definitions
    id = Column(u'id', INTEGER(),primary_key=True, nullable=False, doc=u"模版属性id")
    tpl_name = Column('tpl_name', Unicode(length=128), nullable=False, doc=u"模版名")
    attr_name = Column(u'attr_name', Unicode(length=128), nullable=False, doc=u"模版名")
    attr_value = Column(u'attr_value', Unicode(length=1024), nullable=False, doc=u"属性值")
    attr_desc = Column(u'attr__desc', Unicode(length=255), doc=u"属性描述")


class TraOperateLog(DeclarativeBase):
    """操作日志表"""
    __tablename__ = 'tra_operate_log'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"日志id")
    operator_name = Column(u'operator_name', Unicode(32), nullable=False,doc=u"操作员名称")
    operate_ip = Column(u'operate_ip', Unicode(length=128),doc=u"操作员ip")
    operate_time = Column(u'operate_time', Unicode(length=19), nullable=False,doc=u"操作时间")
    operate_desc = Column(u'operate_desc', Unicode(length=1024),doc=u"操作描述")

class TraOssServer(DeclarativeBase):
    """操作日志表
    服务类型 1:master, 0:slave
    """

    __tablename__ = 'tra_oss_server'

    __table_args__ = {}

    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"OSS服务器id")
    name = Column(u'name', Unicode(length=64), nullable=False,doc=u"OSS服务器IP")
    serv_type = Column(u'serv_type', INTEGER(),doc=u"OSS服务器类型，master/slave")
    auth_url = Column(u'auth_url', Unicode(length=255), doc=u"OSS服务器服务认证地址")
    acct_url = Column(u'acct_url', Unicode(length=255), doc=u"OSS服务器服务记账地址")
    admin_url = Column(u'admin_url', Unicode(length=255), doc=u"OSS服务器服务管理地址")
    secret = Column(u'secret', Unicode(length=64), nullable=False, doc=u"共享密钥")
    last_check = Column(u'last_check', Unicode(length=19), nullable=False, doc=u"最后检测")

class TraOSTypes(DeclarativeBase):
    """设备类型"""
    __tablename__ = 'tra_os_types'

    __table_args__ = {}

    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, doc=u"编号")
    os_name = Column(u'os_name', Unicode(length=32), nullable=False, doc=u"操作系统类型")
    dev_type = Column(u'dev_type', Unicode(length=32), nullable=False, doc=u"设备类型")
    match_rule = Column(u'match_rule', Unicode(length=255), nullable=False, doc=u"匹配规则")


class TraOnline(DeclarativeBase):
    """用户在线信息表 """
    __tablename__ = 'tra_online'

    __table_args__ = {
        'mysql_engine': 'MEMORY'
    }

    # column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, doc=u"在线id")
    username = Column(u'username', Unicode(length=32), nullable=False, index=True, doc=u"上网账号")
    nas_addr = Column(u'nas_addr', Unicode(length=32), nullable=False, index=True, doc=u"bas地址")
    session_id = Column(u'session_id', Unicode(length=64), nullable=False, index=True, doc=u"会话id")
    start_time = Column(u'start_time', Unicode(length=19), nullable=False, doc=u"会话开始时间")
    ipaddr = Column(u'ipaddr', Unicode(length=32),  nullable=False, doc=u"IP地址")
    macaddr = Column(u'macaddr', Unicode(length=32), nullable=False, doc=u"mac地址")
    nas_port_id = Column(u'nas_port_id', Unicode(length=255), nullable=True, doc=u"接入端口物理信息")
    input_total = Column(u'input_total', INTEGER(), doc=u"上行流量（kb）")
    output_total = Column(u'output_total', INTEGER(), doc=u"下行流量（kb）")
    start_source = Column(u'start_source', Unicode(length=64), nullable=False, doc=u"上线来源")


