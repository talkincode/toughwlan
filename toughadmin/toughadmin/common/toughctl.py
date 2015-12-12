#!/usr/bin/env python
# -*- coding: utf-8 -*-
from toughadmin.common import choosereactor
choosereactor.install_optimal_reactor(True)
import argparse, ConfigParser
from toughadmin.common import config as iconfig
from toughadmin.common.shell import shell
from toughadmin.common.dbengine import get_engine
from toughadmin.common import initdb as init_db
import sys, os, signal
import tempfile
import time



def run_admin(config):
    from toughadmin.console import main_app
    main_app.run(config)


def run_initdb(config):
    init_db.update(get_engine(config))


def run_gensql(config):
    from sqlalchemy import create_engine
    def _e(sql, *multiparams, **params): print (sql)

    engine = create_engine(
        config.database.dburl,
        strategy='mock',
        executor=_e
    )
    from toughradius.console import models
    metadata = models.get_metadata(engine)
    metadata.create_all(engine)


def run_dumpdb(config, dumpfs):
    from toughradius.tools import backup
    backup.dumpdb(config, dumpfs)


def run_restoredb(config, restorefs):
    from toughradius.tools import backup
    backup.restoredb(config, restorefs)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-admin', '--admin', action='store_true', default=False, dest='admin', help='run admin')
    parser.add_argument('-port', '--port', type=int, default=0, dest='port', help='handlers port')
    parser.add_argument('-initdb', '--initdb', action='store_true', default=False, dest='initdb', help='run initdb')
    parser.add_argument('-dumpdb', '--dumpdb', type=str, default=None, dest='dumpdb', help='run dumpdb')
    parser.add_argument('-restoredb', '--restoredb', type=str, default=None, dest='restoredb', help='run restoredb')
    parser.add_argument('-gensql', '--gensql', action='store_true', default=False, dest='gensql',
                        help='export sql script file')
    parser.add_argument('-debug', '--debug', action='store_true', default=False, dest='debug', help='debug option')
    parser.add_argument('-x', '--xdebug', action='store_true', default=False, dest='xdebug', help='xdebug option')
    parser.add_argument('-c', '--conf', type=str, default="/etc/toughadmin.conf", dest='conf', help='config file')
    args = parser.parse_args(sys.argv[1:])

    config = iconfig.find_config(args.conf)

    if args.debug or args.xdebug:
        config.defaults.debug = True


    if args.port > 0:
        config.admin.port = args.port

    if args.gensql:
        return run_gensql(config)

    if args.dumpdb:
        return run_dumpdb(config, args.dumpdb)

    if args.restoredb:
        return run_restoredb(config, args.restoredb)

    if args.admin:
        run_admin(config)
    elif args.initdb:
        run_initdb(config)
    else:
        print 'do nothing'
    
        

    
    
    


