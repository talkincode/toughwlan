#!/usr/bin/env python
# coding:utf-8
import json
import re
import time
import urlparse
import urllib
import traceback
from hashlib import md5
import cyclone.auth
import cyclone.escape
import cyclone.web
from mako.template import Template
from twisted.python import log
from cyclone.util import ObjectDict
from cyclone import httpclient
from twisted.internet import defer
from toughportal.common import utils, requests
from toughportal.common.paginator import Paginator

class BaseHandler(cyclone.web.RequestHandler):
    
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.syslog = self.application.syslog
        self.mcache = self.application.mcache
        self.cache_expirt = int(self.settings.config.portal.cache_expire)
        self.get_cache_key = "toughwlan.toughportal.{0}".format

    def check_xsrf_cookie(self):
        pass

    def initialize(self):
        self.tp_lookup = self.application.tp_lookup
        
    def on_finish(self):
        pass
        
    def get_error_html(self, status_code=500, **kwargs):
        if status_code == 404:
            return self.render_string("error.html", msg=u"404:页面不存在")
        elif status_code == 403:
            return self.render_string("error.html", msg=u"403:非法的请求")
        elif status_code == 500:
            if self.settings['debug']:
                return self.render_string("error.html", msg=traceback.format_exc())
            return self.render_string("error.html", msg=u"500:服务器处理失败，请联系管理员")
        else:
            return self.render_string("error.html", msg=u"%s:服务器处理失败，请联系管理员" % status_code)

    def render(self, template_name, **template_vars):
        html = self.render_string(template_name, **template_vars)
        self.write(html)

    def render_error(self, **template_vars):
        self.syslog.error("render template error: {0}".format(repr(template_vars)))
        tpl_name = template_vars.get("tpl_name","")
        tpl = self.get_error_template(tpl_name)
        html = self.render_string(tpl, **template_vars)
        self.write(html)

    def render_json(self, **template_vars):
        if not template_vars.has_key("code"):
            template_vars["code"] = 0
        resp = json.dumps(template_vars, ensure_ascii=False)
        self.write(resp)


    def render_string(self, template_name, **template_vars):
        template_vars["xsrf_form_html"] = self.xsrf_form_html
        template_vars["current_user"] = self.current_user
        template_vars["login_time"] = self.get_secure_cookie("portal_logintime")
        template_vars["request"] = self.request
        template_vars["requri"] = "{0}://{1}".format(self.request.protocol, self.request.host)
        template_vars["handler"] = self
        template_vars["utils"] = utils
        try:
            mytemplate = self.tp_lookup.get_template(template_name)
            return mytemplate.render(**template_vars)
        except Exception as err:
            self.syslog.error("Render template error {0}".format(utils.safestr(err)))
            raise


    def render_from_string(self, template_string, **template_vars):
        template = Template(template_string)
        return template.render(**template_vars)


    def get_page_data(self, query):
        page_size = self.application.settings.get("page_size",20)
        page = int(self.get_argument("page", 1))
        offset = (page - 1) * page_size
        result = query.limit(page_size).offset(offset)
        page_data = Paginator(self.get_page_url, page, query.count(), page_size)
        page_data.result = result
        return page_data
   


    def get_page_url(self, page, form_id=None):
        if form_id:
            return "javascript:goto_page('%s',%s);" %(form_id.strip(),page)
        path = self.request.path
        query = self.request.query
        qdict = urlparse.parse_qs(query)
        for k, v in qdict.items():
            if isinstance(v, list):
                qdict[k] = v and v[0] or ''

        qdict['page'] = page
        return path + '?' + urllib.urlencode(qdict)
        
    def get_current_user(self):
        username = self.get_secure_cookie("portal_user")
        if not username:
            return None
        ipaddr = self.get_secure_cookie("portal_user_ip")

        user = ObjectDict()
        user.username = username
        user.ipaddr = ipaddr
        return user


    def chk_mobile(self):
        userAgent = self.request.headers['User-Agent']
        # userAgent = env.get('HTTP_USER_AGENT')
        _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)' \
                        r'|kindle|midp|mmp|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|' \
                        r'symbian|treo|up\.(browser|link)|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
        _long_matches = re.compile(_long_matches, re.IGNORECASE)
        _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|' \
                         r'ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|' \
                         r'avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|' \
                         r'cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|' \
                         r'ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|' \
                         r'g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|' \
                         r'hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|' \
                         r'ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|' \
                         r'klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|' \
                         r'lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|' \
                         r'mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|' \
                         r'n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|' \
                         r'op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|' \
                         r'pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|' \
                         r'r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|' \
                         r'se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|' \
                         r'so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|' \
                         r'tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|' \
                         r'veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|' \
                         r'w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-'
        _short_matches = re.compile(_short_matches, re.IGNORECASE)
     
        if _long_matches.search(userAgent) is not None:
            return True
        user_agent = userAgent[0:4]
        if _short_matches.search(user_agent) is not None:
            return True
        return False

    @defer.inlineCallbacks
    def chk_os(self):

        chk_funcs = yield self.get_check_os_funs()

        def check_os(user_agent):
            for func in chk_funcs:
                if func[2].search(user_agent) is not None:
                    return func[0], func[1]
            return 'unknow', 'unknow'

        try:
            userAgent = self.request.headers['User-Agent']
            self.syslog.info("UserAgent : %s"% userAgent)
            defer.returnValue(check_os(userAgent))
        except:
            defer.returnValue(('unknow', 'unknow'))


    def get_portal_name(self):
        return u"ToughWLAN"

    def mksign(self, params=[]):
        _params = [str(p) for p in params if p is not None]
        _params.sort()
        print self.settings.config.api
        _params.insert(0, self.settings.config.api.apikey)

        strs = ''.join(_params)
        if self.settings.debug:
            log.msg("sign_src = %s" % strs)
        return md5(strs.encode()).hexdigest().upper()


    def get_wlan_params(self, query_str):
        query_str = urllib.unquote(query_str)
        params = urlparse.parse_qs(query_str)
        param_dict = {k: params[k][0] for k in params}
        return  param_dict

    def get_login_template(self, tpl_name=None):
        return "%s/login.html" % tpl_name


    def get_error_template(self, tpl_name=None):
        if tpl_name:
            return "%s/error.html" % tpl_name
        else:
            return "error.html"

    def get_index_template(self, tpl_name=None):
        if tpl_name:
            return "%s/index.html" % tpl_name
        else:
            return "index.html"

    @defer.inlineCallbacks
    def get_template_attrs(self, ssid):
        cache_key = self.get_cache_key('{0}.{1}'.format('get_template_attrs', ssid))
        _, _resp = yield self.mcache.getPickled(cache_key, uncompress=True)
        if _resp:
            if self.settings.debug:
                self.syslog.debug("query template request hit cache; key=%s" % cache_key)
            defer.returnValue(_resp)

        sign = self.mksign(params=[ssid])
        reqdata = json.dumps(dict(ssid=ssid, sign=sign))
        apiurl = "%s/tpl/query" % self.settings.config.api.apiurl
        if self.settings.debug:
            self.syslog.debug("query template request (%s):  %s" % (apiurl, reqdata))
        resp = yield httpclient.fetch(apiurl, postdata=reqdata, headers={"Content-Type": ["application/json"]})

        jsonresp = json.loads(resp.body)
        if jsonresp['code'] == 1:
            self.syslog.error("query template attrs error, %s" % jsonresp['msg'])
            defer.returnValue({'tpl_name': 'default'})
            return

        if jsonresp['code'] == 0:
            self.syslog.info("query template attrs success")
            self.mcache.setPickled(cache_key, jsonresp['attrs'], compress=True, expireTime=self.cache_expirt)
            defer.returnValue(jsonresp['attrs'])

    @defer.inlineCallbacks
    def get_nas(self, ipaddr):
        cache_key = self.get_cache_key("get_nas_{0}".format(ipaddr))
        _, _resp = yield self.mcache.getPickled(cache_key, uncompress=True)
        if _resp:
            if self.settings.debug:
                self.syslog.debug("query nas server request hit cache; key=%s" % cache_key)
            defer.returnValue(_resp)
            return

        nonce = str(time.time())
        sign = self.mksign(params=[ipaddr, nonce])
        reqdata = json.dumps(dict(nasaddr=ipaddr, nonce=nonce, sign=sign))
        apiurl = "%s/nas/fetch" % self.settings.config.api.apiurl

        if self.settings.debug:
            self.syslog.debug("start query policy server request (%s):  %s" % (apiurl, reqdata))

        resp = yield requests.post(apiurl, data=reqdata, headers={"Content-Type": ["application/json"]})
        jsonresp = yield resp.json()

        if jsonresp['code'] == 1:
            self.syslog.error(jsonresp['msg'])
            defer.returnValue({})

        if jsonresp['code'] == 0:
            self.syslog.info("query policy server success,{0}".format(utils.safestr(jsonresp)))
            self.mcache.setPickled(cache_key, jsonresp, compress=True, expireTime=self.cache_expirt)
            defer.returnValue(jsonresp)

    @defer.inlineCallbacks
    def get_domain(self, ssid):
        cache_key = self.get_cache_key("get_domain")
        _, _resp = yield self.mcache.getPickled(cache_key, uncompress=True)
        if _resp:
            if self.settings.debug:
                self.syslog.debug("query domain request hit cache; key=%s" % cache_key)
            defer.returnValue(_resp)

        sign = self.mksign(params=[ssid])
        reqdata = json.dumps(dict(ssid=ssid, sign=sign))
        apiurl = "%s/domain/query" % self.settings.config.api.apiurl
        if self.settings.debug:
            self.syslog.debug("start query domain request (%s):  %s" % (apiurl, reqdata))
        resp = yield httpclient.fetch(apiurl, postdata=reqdata, headers={"Content-Type": ["application/json"]})

        jsonresp = json.loads(resp.body)
        if jsonresp['code'] == 1:
            self.syslog.error(jsonresp['msg'])
            defer.returnValue(jsonresp['domain'])

        if jsonresp['code'] == 0:
            if self.settings.debug:
                self.syslog.debug("query domain success")
            self.mcache.setPickled(cache_key, jsonresp, compress=True, expireTime=self.cache_expirt)
            defer.returnValue(jsonresp['domain'])

    @defer.inlineCallbacks
    def get_check_os_funs(self):
        cache_key = self.get_cache_key("get_check_os_funs")
        _, _resp = yield self.mcache.getPickled(cache_key, uncompress=True)
        if _resp:
            if self.settings.debug:
                self.syslog.debug("get_check_os_funs request hit cache; key=%s" % cache_key)
            defer.returnValue(_resp)

        sign = self.mksign(params=[self.settings.config.portal.name])
        reqdata = json.dumps(dict(name=self.settings.config.portal.name, sign=sign))

        if self.settings.debug:
            self.syslog.debug("Start query os types request:  %s" % reqdata)

        resp = httpclient.fetch("%s/ostype/query" % self.settings.config.api.apiurl,
                             postdata=reqdata, headers={"Content-Type": ["application/json"]})

        if self.settings.debug:
            self.syslog.debug("query os types resp {}".format(resp.body))

        if resp.code != 200:
            self.syslog.error("query os types from admin server error,http status = %s" % resp.code)
            return

        jsonresp = json.loads(resp.body)
        if jsonresp['code'] == 1:
            self.syslog.error("query os types error, %s" % jsonresp['msg'])
            defer.returnValue([])

        check_os_funcs = []
        for os_name, dev_type, rule in jsonresp['rules']:
            check_os_funcs.append([dev_type, os_name, re.compile(r'{0}'.format(rule), re.IGNORECASE)])

        self.mcache.setPickled(cache_key, check_os_funcs, compress=True, expireTime=self.cache_expirt)
        defer.returnValue(check_os_funcs)


class HomeHandler(BaseHandler):
    def get(self):
        tpl_name = self.get_argument("tpl_name")
        self.render(self.get_index_template(tpl_name))






