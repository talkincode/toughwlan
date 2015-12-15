#!/usr/bin/env python
# coding:utf-8

import os
import ConfigParser


class ConfigDict(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError, k

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k

    def __repr__(self):
        return '<ConfigDict ' + dict.__repr__(self) + '>'


class Config():
    """ Config Object """

    def __init__(self, conf_file=None, **kwargs):

        cfgs = [conf_file, '/etc/toughportal.conf']
        self.config = ConfigParser.ConfigParser()
        flag = False
        for c in cfgs:
            if c and os.path.exists(c):
                self.config.read(c)
                self.filename = c
                flag = True
                break
        if not flag:
            raise Exception("no config")

        self.defaults = ConfigDict(**{k: v for k, v in self.config.items("DEFAULT")})
        self.api = ConfigDict(**{k: v for k, v in self.config.items("api") if k not in self.defaults})
        self.memcached = ConfigDict(**{k: v for k, v in self.config.items("memcached") if k not in self.defaults})
        self.portal = ConfigDict(**{k: v for k, v in self.config.items("portal") if k not in self.defaults})

        self.defaults.debug = self.defaults.debug in ("1", "true")
        self.setup_env()

    def setup_env(self):

        _syslog_enable = os.environ.get("SYSLOG_ENABLE")
        _syslog_server = os.environ.get("SYSLOG_SERVER")
        _syslog_port = os.environ.get("SYSLOG_PORT")
        _syslog_level = os.environ.get("SYSLOG_LEVEL")
        _timezone = os.environ.get("TIMEZONE")
        _api_url = os.environ.get("API_URL")
        _api_key = os.environ.get("API_KEY")


        if _syslog_enable:
            self.defaults.syslog_enable = _syslog_enable
        if _syslog_server:
            self.defaults.syslog_server = _syslog_server
        if _syslog_port:
            self.defaults.syslog_port = _syslog_port
        if _syslog_level:
            self.defaults.syslog_level = _syslog_level
        if _timezone:
            self.defaults.tz = _timezone

        if _api_url:
            self.api.api_url = _api_url
        if _api_key:
            self.api.api_key = _api_key

    def update(self):
        """ update config file"""
        for k, v in self.defaults.iteritems():
            self.config.set("DEFAULT", k, v)

        for k, v in self.api.iteritems():
            if k not in self.defaults:
                self.config.set("api", k, v)

        for k, v in self.memcached.iteritems():
            if k not in self.defaults:
                self.config.set("memcached", k, v)

        for k, v in self.portal.iteritems():
            if k not in self.defaults:
                self.config.set("radiusd", k, v)

        with open(self.filename, 'w') as cfs:
            self.config.write(cfs)


def find_config(conf_file=None):
    return Config(conf_file)

if __name__ == "__main__":
    pass





