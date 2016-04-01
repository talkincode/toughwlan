#!/usr/bin/env python
import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from fabric.api import *
from toughwlan import __version__


def tag():
    local("git tag -a v%s -m 'version %s'"%(__version__,__version__))
    local("git push origin v%s:v%s"%(__version__,__version__))

def all():
    local("venv/bin/python wlanctl standalone -c etc/toughwlan.json")

def push():
    message = raw_input("commit msg:")
    local("git add .")
    local("git commit -m '%s'"%message)
    local("git push origin master")

