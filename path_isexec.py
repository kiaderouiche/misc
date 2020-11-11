#!/usr/bin/env python3
#

import os
import stat

def __path_is_executable(path):
    mode = os.stat(path).st_mode
    return mode & stat.S_IEXEC

def find_prog(program):
    etat_program = __path_is_executable(program)
    if etat_program and not os.path.isdir(program):
        print(program)
    else:
        print("None")

if __name__ == '__main__':
    find_prog("/etc/group")
