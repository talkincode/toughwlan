#!/usr/bin/env python
# coding=utf-8

from toughlib.utils import safestr
from toughwlan.manage.api.api_base import ApiHandler
from toughlib.permit import permit
from toughwlan import models

@permit.route(r"/api/online/query")
class OnlineQueryHandler(ApiHandler):

    def post(self):
        try:
            req_msg = self.parse_request()
        except Exception as err:
            self.render_json(code=1, msg=safestr(err.message))
            return

        session_id = req_msg.get("session_id")
        if not session_id:
            self.render_json(code=1, msg="session_id is empty")

        session = self.db.query(models.TrwOnline).filter_by(session_id=session_id)

        result = dict(
            username=session.username,
            nas_addr=session.nas_addr,
            session_id=session_id,
            start_time=session.start_time,
            ipaddr=session.ipaddr,
            macaddr=session.macaddr,
            input_total=session.input_total,
            output_total=session.output_total
        )

        self.render_json(code=0, msg="success", data=result)

@permit.route(r"/api/online/exists")
class OnlineExistsHandler(ApiHandler):

    def post(self):
        try:
            req_msg = self.parse_request()
        except Exception as err:
            self.render_json(code=1, msg=safestr(err.message))
            return

        session_id = req_msg.get("session_id")
        if not session_id:
            self.render_json(code=1, msg="session_id is empty")

        _exists = self.db.query(models.TrwOnline.id).filter_by(session_id=session_id).count() > 0

        if _exists:
            self.render_json(code=0, msg="session exists")
        else:
            self.render_json(code=1, msg="session not exists")


@permit.route(r"/api/online/delete")
class OnlineDeleteHandler(ApiHandler):

    def post(self):
        try:
            req_msg = self.parse_request()
        except Exception as err:
            self.render_json(code=1, msg=safestr(err.message))
            return

        session_id = req_msg.get("session_id")
        if not session_id:
            self.render_json(code=1, msg="session_id is empty")

        self.db.query(models.TrwOnline).filter_by(session_id=session_id).delete()
        self.render_json(code=0, msg="success")





