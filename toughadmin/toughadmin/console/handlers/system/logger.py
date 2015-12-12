#!/usr/bin/env python
# coding:utf-8
import os.path
import cyclone.auth
import cyclone.escape
import cyclone.web
from toughadmin.console.handlers.base import BaseHandler, MenuSys
from toughadmin.common.permit import permit

def log_query(logfile):
    if os.path.exists(logfile):
        with open(logfile) as f:
            f.seek(0, 2)
            if f.tell() > 32 * 1024:
                f.seek(f.tell() - 32 * 1024)
            else:
                f.seek(0)
            return f.read().replace('\n', '<br>')
    else:
        return "logfile %s not exist" % logfile

@permit.route(r"/logger", u"系统日志查询", MenuSys, order=1.0500, is_menu=True)
class LoggerHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        logfile = "/var/toughadmin/log/admin.log"
        return self.render("logger.html", msg=log_query(logfile), title="handlers logging", logfile=logfile)


