#!/usr/bin/env python
# -*- coding: utf-8 -*-
from toughlib import choosereactor
choosereactor.install_optimal_reactor(True)
from twisted.python import log
from twisted.internet import reactor
from toughlib import config as iconfig
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

def check_env(config):
    try:
        backup_path = config.database.backup_path
        if not os.path.exists(backup_path):
            os.system("mkdir -p  %s" % backup_path)
        if not os.path.exists("/var/toughwlan"):
            os.system("mkdir -p /var/toughwlan")
        if not os.path.exists("/var/toughwlan/.install"):
            start_initdb(config)
            os.system("touch /var/toughwlan/.install ")
    except Exception as err:
        import traceback
        traceback.print_exc()

def start_initdb(config):
    from toughwlan.common import initdb as init_db
    init_db.update(config)

def start_admin(config,log):
    from toughwlan.admin import webserver
    from toughwlan.admin import ddns_task
    webserver.run(config, log)
    ddns_task.run(config, log)

def start_portal(config,log):
    from toughwlan.portal import portald, webserver
    portald.run(config,log)
    webserver.run(config,log)

def start_acagent(config,log):
    from toughwlan.acagent import authorized, portald, webserver
    authorized.run(config, log)
    portald.run(config, log)
    webserver.run(config, log)


def run():
    log.startLogging(sys.stdout)
    parser = argparse.ArgumentParser()
    parser.add_argument('-admin', '--admin', action='store_true', default=False, dest='admin', help='run admin')
    parser.add_argument('-portal', '--portal', action='store_true', default=False, dest='portal', help='run portal')
    parser.add_argument('-acagent', '--acagent', action='store_true', default=False, dest='acagent', help='run acagent')
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

    if args.admin:
        start_admin(config,syslog)
        reactor.run()    

    elif args.portal:
        start_portal(config,syslog)
        reactor.run()

    elif args.acagent:
        start_acagent(config,syslog)
        reactor.run()

    elif args.standalone:
        start_admin(config,syslog)
        start_portal(config,syslog)
        start_acagent(config,syslog)
        reactor.run()

    elif args.initdb:
        start_initdb(config)

    else:
        parser.print_help()
    
        

    
    
    


