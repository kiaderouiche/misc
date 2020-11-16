# FindProgram.py
#
# Copyright (C) 2007 Carlos Garcia Campos <carlosgc@gsyc.escet.urjc.es>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os
import pathlib
import stat


def find_program(program):
    '''Looks for given program in current path.
    Returns an absolute path if program was found or None'''

    def __path_is_executable(path):
        return os.stat(path).st_mode & stat.S_IEXEC

    # Do not look in PATH if it's already an absolute path
    # or a relative path containing directories
    if pathlib.PurePosixPath(program).is_absolute() or program.find(os.path.sep) > 0:
        if __path_is_executable(program) and not pathlib.Path(program).is_dir():
            return program
        else:
            return None

    # Look in PATH
    try:
        path = os.environ['PATH']
    except KeyError:
        # There is no PATH in env!!!
        # FIXME: it only works on UNIX
        # NetBSD path: /usr/pkg/
        path = "/bin:/usr/bin:/usr/local/bin/:/usr/pkg/bin:."

    for p in path.split(os.pathsep):
        absolute = pathlib.Path().joinpath(p, program)
        if pathlib.Path(absolute).exists() and \
           __path_is_executable(absolute) and \
           not pathlib.Path(absolute).is_dir():
            return absolute

    return None

if __name__ == '__main__':
    import sys

    ## Absolute path
    # Dir
    if find_program(os.environ['HOME']) is not None:
        print ("FAILED")
        sys.exit(1)

    # File not exec
    if find_program('./FindProgram.py') is not None:
        print ("FAILED")
        sys.exit(2)

    # File exec
    if find_program('/bin/ls') != '/bin/ls':
        print ("FAILED")
        sys.exit(3)

    ## Relative path
    if find_program('cat') != '/bin/cat':
        print ("FAILED")
        sys.exit(4)

    print ("SUCCESS")
