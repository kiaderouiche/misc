#!/usr/bin/env python2
#

import os

def __path_is_executable(path):
    mode = os.stat(path).st_mode
    if S_IEXEC(mode):
        return    return os.stat(path)[ST_MODE] & S_IEXEC

def main():
    __path_is_executable('/etc/group')

if __name__ == '__main__':
    main()
