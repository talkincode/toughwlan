#!/usr/bin/env python
#coding=utf-8

import re

check_funcs = [
    [ "Phone","ios", re.compile(r'iPod', re.IGNORECASE) ],
    [ "Pad","ios",re.compile(r'iPad', re.IGNORECASE) ],
    [ "PC","OSX",re.compile(r'Intel Mac', re.IGNORECASE) ],
    [ "Phone","ios",re.compile(r'iPhone', re.IGNORECASE) ],
    [ "Phone","symbian",re.compile(r'symbian', re.IGNORECASE) ],
    [ "Phone","android1",re.compile(r'Android 1', re.IGNORECASE) ],
    [ "Phone", "android2",re.compile(r'Android 2', re.IGNORECASE) ],
    [ "Phone", "android3",re.compile(r'Android 3', re.IGNORECASE) ],
    [ "Phone", "android4",re.compile(r'Android 4', re.IGNORECASE) ],
    [ "PC", "win2000",re.compile(r'Windows NT 5.0', re.IGNORECASE) ],
    [ "PC","winxp",re.compile(r'Windows NT 5.1', re.IGNORECASE) ],
    [ "PC","win2003",re.compile(r'Windows NT 5.2', re.IGNORECASE) ],
    [ "PC","winvista",re.compile(r'Windows NT 6.0', re.IGNORECASE) ],
    ["PC", "win7", re.compile(r'Windows NT 6.1', re.IGNORECASE)],
    [ "PC","win8",re.compile(r'Windows NT 6.2', re.IGNORECASE) ],
    [ "Phone","winphone", re.compile(r'Windows Phone', re.IGNORECASE) ],
    [ "Phone","BlackBerry",re.compile(r'BlackBerry', re.IGNORECASE) ],
    [ "PC","linux",re.compile(r'x11', re.IGNORECASE) ]
]

def check_os(user_agent):
    for func in check_funcs:
        if func[2].search(user_agent)!=None:
            return func[0],func[1]

    return 'unknow','unknow'


if __name__ == '__main__':
    print check_os('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)')