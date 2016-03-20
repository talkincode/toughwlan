#!/usr/bin/env python
import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from fabric.api import *
from toughwlan import __version__


def tag():
    local("git tag -a v%s -m 'version %s'"%(__version__,__version__))
    local("git push origin v%s:v%s"%(__version__,__version__))

def httpd():
    local("pypy toughctl --httpd -c etc/toughwlan.json")

def portald():
    local("pypy toughctl --portald -c etc/toughwlan.json")

def all():
    local("pypy toughctl --standalone -c etc/toughwlan.json")

def push():
    message = raw_input("commit msg:")
    local("git add .")
    local("git commit -m '%s'"%message)
    local("git push origin master")
    local("git push src master")

def initdb():
    local("pypy toughctl --initdb -c etc/toughwlan.json")

def uplib():
    local("pypy -m pip install https://github.com/talkincode/toughlib/archive/master.zip --upgrade --no-deps")

def uplib2():
    local("pypy -m pip install https://github.com/talkincode/txportal/archive/master.zip --upgrade --no-deps")

def uplib3():
    local("pypy -m pip install https://github.com/talkincode/txradius/archive/master.zip --upgrade --no-deps")