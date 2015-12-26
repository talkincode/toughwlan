#!/usr/bin/env python
# -*- coding: utf-8 -*-
from toughlib import choosereactor
choosereactor.install_optimal_reactor(True)
import argparse
from toughlib import config as iconfig
from toughwlan.common import initdb as init_db
from toughwlan.tasks import portal_ping, radius_ping, oss_ping
from toughwlan.console import main_app
import sys

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-admin', '--admin', action='store_true', default=False, dest='admin', help='run admin')
    parser.add_argument('-port', '--port', type=int, default=0, dest='port', help='admin port')
    parser.add_argument('-initdb', '--initdb', action='store_true', default=False, dest='initdb', help='run initdb')
    parser.add_argument('-debug', '--debug', action='store_true', default=False, dest='debug', help='debug option')
    parser.add_argument('-c', '--conf', type=str, default="/etc/toughwlan.json", dest='conf', help='config file')
    args = parser.parse_args(sys.argv[1:])

    config = iconfig.find_config(args.conf)

    if args.debug:
        config.system.debug = True

    if args.port > 0:
        config.admin.port = args.port

    if args.admin:
        main_app.run(config)
    elif args.initdb:
        init_db.update(config)
    else:
        parser.print_help()
    
        

    
    
    


