#!/usr/bin/env python2
#

import os

def __path_is_executable(path):
    return os.stat(path)[ST_MODE] & S_IEXEC

def main():
    __path_is_executable('/etc/group')

if __name__ == '__main__':
    main()
