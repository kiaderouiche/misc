#!/usr/bin/env python3
#

import os

def __path_is_executable(path):
    mode = os.stat(path).st_mode
    return os.path.isfile(path) and os.access(path, mode)
    #os.stat(path)[ST_MODE] & S_IEXEC

def main():
    __path_is_executable('/etc/group')

if __name__ == '__main__':
    main()
