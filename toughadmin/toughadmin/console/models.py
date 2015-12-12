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
    ip_addr = Column(u'ip_addr', Unicode(length=15), nullable=False, index=True,  doc=u"IP地址")
    bas_name = Column(u'bas_name', Unicode(length=64), nullable=False, doc=u"bas名称")
    bas_secret = Column(u'bas_secret', Unicode(length=64), nullable=False, doc=u"共享密钥")
    vendor_id = Column(u'vendor_id', SMALLINT(), nullable=False, doc=u"bas类型")
    portal_vendor = Column(u'portal_vendor', Unicode(length=64), nullable=False, doc=u"portal协议")
    time_type = Column(u'time_type', SMALLINT(), nullable=False, doc=u"时区类型")
    ac_port = Column(u'ac_port', INTEGER(), nullable=False, doc=u"AC端口")
    coa_port = Column(u'coa_port', INTEGER(), nullable=False, doc=u"CoA端口")

    # relation definiti


class TraRadius(DeclarativeBase):
    """radius节点表 """
    __tablename__ = 'tra_radius'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"设备id")
    ip_addr = Column(u'ip_addr', Unicode(length=15), nullable=False,doc=u"IP地址")
    name = Column(u'name', Unicode(length=64), nullable=False, doc=u"radius名称")
    admin_port = Column(u'admin_port', INTEGER(), nullable=False, doc=u"管理端口")
    secret = Column(u'secret', Unicode(length=64), nullable=False,doc=u"共享密钥")
    auth_port = Column(u'auth_port', INTEGER(), nullable=False, doc=u"认证端口")
    acct_port = Column(u'acct_port', INTEGER(), nullable=False, doc=u"记账端口")
    status = Column(u'status', INTEGER(), nullable=False, doc=u"状态,0/1")
    last_check = Column(u'last_check', Unicode(length=19), nullable=True, doc=u"最后检测")


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


class TraStatus(DeclarativeBase):
    """radius状态信息表 """
    __tablename__ = 'tra_status'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"id")
    radius_name = Column(u'radius_name', Unicode(length=16), nullable=False,doc=u"radius名称")
    auth_all = Column(u'auth_all', INTEGER(), nullable=False, doc=u"认证总数")
    auth_accept = Column(u'auth_accept', INTEGER(), nullable=False, doc=u"认证成功数")
    auth_reject = Column(u'auth_reject', INTEGER(), nullable=False, doc=u"认证拒绝数")
    acct_all = Column(u'acct_all', INTEGER(), nullable=False, doc=u"记账总数")
    acct_start = Column(u'acct_start', INTEGER(), nullable=False, doc=u"记账开始数")
    acct_stop = Column(u'acct_stop', INTEGER(), nullable=False, doc=u"记账结束数")
    acct_update = Column(u'acct_update', INTEGER(), nullable=False, doc=u"记账更新数")
    acct_on = Column(u'acct_on', INTEGER(), nullable=False, doc=u"记账上线数")
    acct_off = Column(u'acct_off', INTEGER(), nullable=False, doc=u"记账下线数")



class TraPortal(DeclarativeBase):
    """portal节点表 """
    __tablename__ = 'tra_portal'

    __table_args__ = {}

    # column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, doc=u"设备id")
    ip_addr = Column(u'ip_addr', Unicode(length=15), nullable=False, doc=u"IP地址")
    name = Column(u'name', Unicode(length=64), nullable=False, doc=u"radius名称")
    admin_port = Column(u'admin_port', INTEGER(), nullable=False, doc=u"管理端口")
    secret = Column(u'secret', Unicode(length=64), nullable=False, doc=u"共享密钥")
    http_port = Column(u'http_port', INTEGER(), nullable=False, doc=u"http认证端口")
    listen_port = Column(u'listen_port', INTEGER(), nullable=False, doc=u"监听端口")
    status = Column(u'status', INTEGER(), nullable=False, doc=u"状态,0/1")
    last_check = Column(u'last_check', Unicode(length=19), nullable=True, doc=u"最后检测")


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
    服务类型 0:master, 2:slave
    """

    __tablename__ = 'tra_oss_server'

    __table_args__ = {}

    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"OSS服务器id")
    ipaddr = Column(u'ipaddr', Unicode(15), nullable=False,doc=u"OSS服务器IP")
    serv_type = Column(u'serv_type', INTEGER(),doc=u"OSS服务器类型，master/slave")
    admin_port = Column(u'admin_port', INTEGER(),doc=u"OSS服务器服务管理端口")
    auth_port = Column(u'auth_port', INTEGER(),doc=u"OSS服务器服务认证端口")
    acct_port = Column(u'acct_port', INTEGER(), doc=u"OSS服务器服务记账端口")
    secret = Column(u'secret', Unicode(length=64), nullable=False, doc=u"共享密钥")
    status = Column(u'status', INTEGER(), nullable=False, doc=u"状态")

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


class TraAccount(DeclarativeBase):
    """
    account_number 为每个套餐对应的上网账号，每个上网账号全局唯一
    用户状态 1:"正常", 2:"停机"
    """

    __tablename__ = 'tra_account'

    __table_args__ = {}

    account_number = Column('account_number', Unicode(length=32), primary_key=True, nullable=False, doc=u"上网账号")
    password = Column('password', Unicode(length=128), nullable=False, doc=u"上网密码")
    status = Column('status', INTEGER(), nullable=False, doc=u"用户状态")
    realname = Column('realname', Unicode(length=64), nullable=False, doc=u"")
    idcard = Column('idcard', Unicode(length=32), doc=u"用户证件号码")
    sex = Column('sex', SMALLINT(), nullable=True, doc=u"用户性别0/1")
    age = Column('age', INTEGER(), nullable=True, doc=u"用户年龄")
    email = Column('email', Unicode(length=255), nullable=True, doc=u"用户邮箱")
    mobile = Column('mobile', Unicode(length=16), nullable=True, index=True, doc=u"用户手机")
    address = Column('install_address', Unicode(length=128), nullable=False, doc=u"装机地址")
    balance = Column('balance', INTEGER(), nullable=False, doc=u"用户余额-分")
    time_length = Column('time_length', INTEGER(), nullable=False, default=0, doc=u"用户时长-秒")
    flow_length = Column('flow_length', INTEGER(), nullable=False, default=0, doc=u"用户流量-kb")
    expire_date = Column('expire_date', Unicode(length=10), nullable=False, index=True, doc=u"过期时间- ####-##-##")
    concur_number = Column('concur_number', INTEGER(), nullable=False, doc=u"用户并发数")
    bind_mac = Column('bind_mac', SMALLINT(), nullable=False, doc=u"是否绑定mac")
    bind_vlan = Column('bind_vlan', SMALLINT(), nullable=False, doc=u"是否绑定vlan")
    mac_addr = Column('mac_addr', Unicode(length=17), doc=u"mac地址")
    vlan_id = Column('vlan_id', INTEGER(), doc=u"内层vlan")
    vlan_id2 = Column('vlan_id2', INTEGER(), doc=u"外层vlan")
    ip_addr = Column('ip_addr', Unicode(length=15), index=True, doc=u"静态IP地址")
    up_limit = Column('up_limit', INTEGER(), nullable=False, doc=u"上行速率限制 bps")
    down_limit = Column('down_limit', INTEGER(), nullable=False, doc=u"下行速率限制 bps")
    account_desc = Column('account_desc', Unicode(255), doc=u"用户描述")
    create_time = Column('create_time', Unicode(length=19), nullable=False, index=True, doc=u"创建时间")
    update_time = Column('update_time', Unicode(length=19), nullable=False, doc=u"更新时间")


class TraAccountAttr(DeclarativeBase):
    """上网账号扩展策略属性表"""
    __tablename__ = 'tra_account_attr'
    __table_args__ = {}

    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, doc=u"属性id")
    account_number = Column('account_number', Unicode(length=32), nullable=False, index=True, doc=u"上网账号")
    attr_name = Column('attr_name', Unicode(length=255), nullable=False, index=True, doc=u"属性名")
    attr_value = Column('attr_value', Unicode(length=255), nullable=False, doc=u"属性值")
    attr_desc = Column('attr_desc', Unicode(length=255), doc=u"属性描述")