#!/usr/bin/env python
#coding:utf-8
import cyclone.auth
import cyclone.escape
import cyclone.web
from beaker.cache import cache_managers
from toughadmin.console.handlers.base import BaseHandler
from toughadmin.common.permit import permit

@permit.route(r"/")
class HomeHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.render("index.html")

@permit.route(r"/cache/clean")
class CacheCleanHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        for _cache in cache_managers.values():
            _cache.clear()
        return self.render_json(code=0, msg=u"已刷新缓存")





