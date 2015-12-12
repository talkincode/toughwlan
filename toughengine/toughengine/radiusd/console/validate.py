#!/usr/bin/env python
# coding=utf-8


import re
from toughengine.radiusd.utils import safestr

class regexp():
    def __init__(self, rexp=None,test=None, msg=None):
        self.rexp = rexp and re.compile(rexp) or None
        self.test = test
        self.msg = msg

    def valid(self, value):
        if self.rexp:
            return bool(self.rexp.match(safestr(value)))
        if self.test:
            try:
                return self.test(value)
            except:
                return False

not_null = regexp(test=bool,msg=u"不允许为空")
is_not_empty = regexp('.+', msg=u"不允许为空")
is_date = regexp('(\d{4})-(\d{2}-(\d\d))', msg=u"日期格式:yyyy-MM-dd")
is_email = regexp('[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$', msg=u"email格式,比如name@domain.com")
is_chars = regexp("^[A-Za-z]+$", msg=u"必须是英文字符串")
is_alphanum = lambda x: regexp("^[A-Za-z0-9]{%s}$" % x, msg=u"必须是长度为%s的数字字母组合" % x)
is_alphanum2 = lambda x, y: regexp("^[A-Za-z0-9]{%s,%s}$" % (x, y), msg=u"必须是长度为%s到%s的数字字母组合" % (x, y))
is_number = regexp("^[0-9]*$", msg=u"必须是数字")
is_number2 = regexp("^[1-9]\d*$", u'必须是大于0的正整数')
is_number3 = regexp('^(([1-9]\d*)|0)(\.\d{1,3})?$', msg=u"支持包含(最大3位)小数点 xx.xxxxx")
is_numberOboveZore = regexp("^\\d+$", msg=u"必须为大于等于0的整数")
is_cn = regexp("^[\u4e00-\u9fa5],{0,}$", msg=u"必须是汉字")
is_url = regexp('[a-zA-z]+://[^\s]*', msg=u"url格式 xxxx://xxx")
is_phone = regexp('^(\(\d{3,4}\)|\d{3,4}-)?\d{7,8}$', msg=u"固定电话号码格式：0000-00000000")
is_idcard = regexp('^\d{15}$|^\d{18}$|^\d{17}[Xx]$', msg=u"身份证号码格式")
is_ip = regexp("\d+\.\d+\.\d+\.\d+", msg=u"ip格式：xxx.xxx.xxx.xxx")
is_mac = regexp("[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}$", msg=u"MAC地址格式 xx:xx:xx:xx:xx:xx")
is_rmb = regexp('^(([1-9]\d*)|0)(\.\d{1,2})?$', msg=u"人民币金额 xx.xx")
len_of = lambda x, y: regexp("[\s\S]{%s,%s}$" % (x, y), msg=u"长度必须为%s到%s" % (x, y))
is_alphanum3 = lambda x, y: regexp("^[A-Za-z0-9\_\-]{%s,%s}$" % (x, y), msg=u"必须是长度为%s到%s的数字字母与下划线组合" % (x, y))
is_period = regexp("(^$)|^([01][0-9]|2[0-3]):[0-5][0-9]-([01][0-9]|2[0-3]):[0-5][0-9]$",
                           msg=u"时间段，hh:mm-hh:mm,支持跨天，如 19:00-09:20")
is_telephone = regexp("^1[0-9]{10}$", msg=u"必须是手机号码")
is_time = regexp('(\d{4})-(\d{2}-(\d\d))\s([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]',
                         msg=u"时间格式:yyyy-MM-dd hh:mm:ss")
is_time_hm = regexp('^([01][0-9]|2[0-3]):[0-5][0-9]$', msg=u"时间格式: hh:mm")


if __name__ == "__main__":
    print is_mac.valid("00:0C:29:E3:5F:39")
    print not_null.valid(None)
    print is_ip.valid('127.0.0.2')