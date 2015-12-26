#!/usr/bin/env python
#coding:utf-8
from toughwlan.console.handlers.base import BaseHandler
from toughlib.permit import permit

@permit.route(r"/logout")
class LogoutHandler(BaseHandler):

    def get(self):
        if not self.current_user:
            self.clear_all_cookies()
            self.redirect("/login")
            return
        self.clear_all_cookies()    
        self.redirect("/login",permanent=False)


