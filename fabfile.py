#!/usr/bin/env python
import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from fabric.api import *
from toughwlan import __version__


def tag():
    local("git tag -a v%s -m 'version %s'"%(__version__,__version__))
    local("git push origin v%s:v%s"%(__version__,__version__))

def admin():
    local("pypy toughctl --admin -c toughwlan.json")

def portal():
    local("pypy toughctl --portal -c toughwlan.json")

def acagent():
    local("pypy toughctl --acagent -c toughwlan.json")

def all():
    local("pypy toughctl --standalone -c toughwlan.json")

def initdb():
    local("pypy toughctl --initdb -c toughwlan.json")

def uplib():
    local("pypy -m pip install https://github.com/talkincode/toughlib/archive/master.zip --upgrade --no-deps")

def uplib2():
    local("pypy -m pip install https://github.com/talkincode/txportal/archive/master.zip --upgrade --no-deps")

def uplib3():
    local("pypy -m pip install https://github.com/talkincode/txradius/archive/master.zip --upgrade --no-deps")