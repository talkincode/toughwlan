#!/usr/bin/env python
# -*- coding: utf-8 -*-
from toughac.common import choosereactor
choosereactor.install_optimal_reactor(True)
import argparse
from toughac.common import config as iconfig
import sys



def run_cmcc(config):
    from toughac.acagent import cmcc_agent
    cmcc_agent.run(config)

def run_huawei(config):
    from toughac.acagent import huawei_agent
    huawei_agent.run(config)


def run_webauth(config):
    from toughac.portal import webauth
    webauth.run(config)

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-portal', '--portal', action='store_true', default=False, dest='portal', help='run portal')
    parser.add_argument('-webauth', '--webauth', action='store_true', default=False, dest='webauth', help='run webauth')
    parser.add_argument('-vendor', '--vendor', type=str, default="cmcc", dest='vendor', help='run vendor')
    parser.add_argument('-port', '--port', type=int, default=0, dest='port', help='handlers port')
    parser.add_argument('-debug', '--debug', action='store_true', default=False, dest='debug', help='debug option')
    parser.add_argument('-c', '--conf', type=str, default="/etc/toughac.conf", dest='conf', help='config file')
    args = parser.parse_args(sys.argv[1:])

    config = iconfig.find_config(args.conf)

    if args.debug:
        config.defaults.debug=True

    if args.port > 0:
        config.ac.port = args.port

    if args.vendor > 0:
        config.ac.vendor = args.vendor

    if args.portal:
        return run_cmcc(config)
    if args.webauth:
        return run_webauth(config)
    else:
        print 'do nothing'
    
        

    
    
    


