#!/usr/bin/env python
#coding:utf-8
import sys,os
from toughportal.common import utils
import shutil
import time
import random
import ConfigParser

def gen_secret(clen=32):
    rg = random.SystemRandom()
    r = list('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return ''.join([rg.choice(r) for _ in range(clen)])

    