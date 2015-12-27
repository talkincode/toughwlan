#!/usr/bin/env python
# -*- coding: utf-8 -*-
from toughlib import choosereactor
choosereactor.install_optimal_reactor(True)
from twisted.python import log
from twisted.internet import reactor
from toughlib import config as iconfig
from toughwlan.common import initdb as init_db
from toughwlan.common import ddns_task
from toughwlan.console import main_app
from toughwlan.console import portal_app
from toughwlan.console import portal_server
from toughlib import logger
import sys,os
import argparse

def update_timezone(config):
    try:
        if 'TZ' not in os.environ:
            os.environ["TZ"] = config.system.tz
        time.tzset()
    except:
        pass

def run():
    log.startLogging(sys.stdout)
    parser = argparse.ArgumentParser()
    parser.add_argument('-admin', '--admin', action='store_true', default=False, dest='admin', help='run admin')
    parser.add_argument('-portal', '--portal', action='store_true', default=False, dest='portal', help='run portal')
    parser.add_argument('-ddns', '--ddns', action='store_true', default=False, dest='ddns', help='run ddns')
    parser.add_argument('-standalone', '--standalone', action='store_true', default=False, dest='standalone', help='run standalone')
    parser.add_argument('-port', '--port', type=int, default=0, dest='port', help='port')
    parser.add_argument('-initdb', '--initdb', action='store_true', default=False, dest='initdb', help='run initdb')
    parser.add_argument('-debug', '--debug', action='store_true', default=False, dest='debug', help='debug option')
    parser.add_argument('-c', '--conf', type=str, default="/etc/toughwlan.json", dest='conf', help='config file')
    args = parser.parse_args(sys.argv[1:])

    config = iconfig.find_config(args.conf)
    update_timezone(config)

    if args.debug:
        config.system.debug = True

    if args.port > 0:
        config.admin.port = args.port

    syslog = logger.Logger(config)

    if args.admin:
        main_app.run(config, log=syslog)
        reactor.run()    
    elif args.portal:
        portal_app.run(config, log=syslog)
        portal_server.run(config,log=syslog)
        reactor.run()
    elif args.ddns:
        ddns_task.run(config, log=syslog)
        reactor.run()
    elif args.standalone:
        main_app.run(config, log=syslog)
        portal_app.run(config,log=syslog)
        portal_server.run(config,log=syslog)
        ddns_task.run(config, log=syslog)
        reactor.run()
    elif args.initdb:
        init_db.update(config)
    else:
        parser.print_help()
    
        

    
    
    


