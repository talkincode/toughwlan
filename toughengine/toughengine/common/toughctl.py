#!/usr/bin/env python
# coding=utf-8
from autobahn.twisted import choosereactor

choosereactor.install_optimal_reactor(False)
from toughengine.radiusd import radiusd, admin
from toughengine.common import config as iconfig
import argparse
import sys


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-auth', '--auth', action='store_true', default=False, dest='auth', help='run radius auth')
    parser.add_argument('-acct', '--acct', action='store_true', default=False, dest='acct', help='run radius acct')
    parser.add_argument('-admin', '--admin', action='store_true', default=False, dest='admin', help='run radius admin')
    parser.add_argument('-debug', '--debug', action='store_true', default=False, dest='debug', help='debug option')
    parser.add_argument('-c', '--conf', type=str, default="/etc/toughengine.conf", dest='conf', help='config file')
    args = parser.parse_args(sys.argv[1:])

    config = iconfig.Config(args.conf)

    if args.debug:
        config.defaults.debug = True

    if args.auth:
        radiusd.run_auth(config)
    elif args.acct:
        radiusd.run_acct(config)
    elif args.admin:
        admin.run_admin(config)
    else:
        print 'do nothing'
