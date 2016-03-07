#!/usr/bin/env python
# -*- coding: utf-8 -*-
from toughlib import choosereactor
choosereactor.install_optimal_reactor(True)
from twisted.python import log
from twisted.internet import reactor
from toughlib import config as iconfig
from toughlib.dbengine import get_engine
from toughlib import dispatch,logger
import sys,os
import argparse

def update_timezone(config):
    try:
        if 'TZ' not in os.environ:
            os.environ["TZ"] = config.system.tz
        time.tzset()
    except:
        pass

def check_env(config):
    try:
        backup_path = config.database.backup_path
        if not os.path.exists(backup_path):
            os.system("mkdir -p  %s" % backup_path)
        if not os.path.exists("/var/toughwlan"):
            os.system("mkdir -p /var/toughwlan")
    except Exception as err:
        import traceback
        traceback.print_exc()

def start_initdb(config):
    from toughwlan.common import initdb as init_db
    init_db.update(config)

def start_admin(config,dbengine):
    from toughwlan.admin import httpd as admin_web
    from toughwlan.admin import ddns_task
    admin_web.run(config, dbengine)
    ddns_task.run(config, dbengine)

def start_portal(config,dbengine):
    from toughwlan.portal import portald
    from toughwlan.portal import httpd as portal_web
    portald.run(config,dbengine)
    portal_web.run(config,dbengine)

def run():
    log.startLogging(sys.stdout)
    parser = argparse.ArgumentParser()
    parser.add_argument('-admin', '--admin', action='store_true', default=False, dest='admin', help='run admin')
    parser.add_argument('-portal', '--portal', action='store_true', default=False, dest='portal', help='run portal')
    parser.add_argument('-standalone', '--standalone', action='store_true', default=False, dest='standalone', help='run standalone')
    parser.add_argument('-initdb', '--initdb', action='store_true', default=False, dest='initdb', help='run initdb')
    parser.add_argument('-debug', '--debug', action='store_true', default=False, dest='debug', help='debug option')
    parser.add_argument('-c', '--conf', type=str, default="/etc/toughwlan.json", dest='conf', help='config file')
    args = parser.parse_args(sys.argv[1:])

    config = iconfig.find_config(args.conf)
    update_timezone(config)
    check_env(config)

    if args.debug:
        config.system.debug = True

    syslog = logger.Logger(config)
    dbengine = get_engine(config)
    dispatch.register(syslog)

    if args.admin:
        start_admin(config,dbengine=dbengine)
        reactor.run()    

    elif args.portal:
        start_portal(config,dbengine=dbengine)
        reactor.run()

    elif args.standalone:
        start_admin(config,dbengine=dbengine)
        start_portal(config,dbengine=dbengine)
        reactor.run()

    elif args.initdb:
        start_initdb(config)

    else:
        parser.print_help()
    
        

    
    
    


