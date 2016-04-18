#!/usr/bin/env python
#coding:utf-8
import tornado.auth
import tornado.escape
import tornado.web
from beaker.cache import cache_managers
from toughwlan.manage.base import BaseHandler
from toughlib.permit import permit

@permit.route(r"/")
class HomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html", config=self.settings['config'])

@permit.route(r"/cache/clean")
class CacheCleanHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        for _cache in cache_managers.values():
            _cache.clear()
        return self.render_json(code=0, msg=u"已刷新缓存")





