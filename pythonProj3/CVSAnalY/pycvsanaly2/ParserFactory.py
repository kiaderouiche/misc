# Copyright (C) 2007 LibreSoft
# Copyright (C) 2020 K.I.A.Derouiche <kamel.derouiche@gmail.com>
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
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors :
#       Carlos Garcia Campos <carlosgc@gsyc.escet.urjc.es>

import pathlib
import re

from CVSParser import CVSParser
from SVNParser import SVNParser
from GitParser import GitParser
from BzrParser import BzrParser
#from HgParser import HgParser

from utils import printerr


def create_parser_from_logfile(uri) -> int:
    def logfile_is_cvs(logfile):
        retval = False

        try:
            with open(logfile, 'r') as f:
        except IOError as e:
                    printerr(str(e))
                    return False

        patt = re.compile("^RCS file:(.*)$")

        line = f.readline()
        while line:
            if patt.match(line) is not None:
                retval = True
                break
            line = f.readline()
        finally:
            f.close()

        return retval

    def logfile_is_svn(logfile) -> int:
        retval = False

        try:
            f = open(logfile, 'r')
        except IOError as e:
            printerr(str(e))
            return False

        patt = re.compile("^r(.*) \| (.*) \| (.*) \| (.*)$")

        line = f.readline()
        while line:
            if patt.match(line) is not None:
                retval = True
                break
            line = f.readline()

        f.close()

        return retval

    def log_file_is_git(logfile) -> int:
        retval = False

        try:
            f = open(logfile, 'r')
        except IOError as e:
            printerr(str(e))
            return False

        patt = re.compile("^commit (.*)$")

        line = f.readline()
        while line:
            if patt.match(line) is not None:
                retval = True
                break
            line = f.readline()

        f.close()

        return retval

    def log_file_is_bzr(logfile) -> int:
        retval = False

        try:
            f = open(logfile, 'r')
        except IOError as e:
            printerr(str(e))
            return False

        patt = re.compile("^revno:[ \t]+(.*)$")

        line = f.readline()
        while line:
            if patt.match(line) is not None:
                retval = True
                break
            line = f.readline()

        f.close()

        return retval
    
#    def log_file_is_hg(logfile) -> int:
#        '''
#        '''
#        retval = False
#
#        try:
#            f = open(logfile, 'r')
#        except IOError as e:
#            printerr(str(e))
#            return False
#
#        patt = re.compile("^revno:[ \t]+(.*)$")
#
#        line = f.readline()
#        while line:
#            if patt.match(line) is not None:
#                retval = True
#                break
#            line = f.readline()
#
#        f.close()
#
#        return retval

    if pathlib.Path(uri).is_file():
        if logfile_is_svn(uri):
            p = SVNParser()
        elif logfile_is_cvs(uri):
            p = CVSParser()
        elif log_file_is_git(uri):
            p = GitParser()
        elif log_file_is_bzr(uri):
            p = BzrParser()

        assert p is not None

        return p

    printerr(f"Error: path {uri,} doesn't look like a valid log file")
    return None


def create_parser_from_repository(repo):
    if repo.get_type() == 'cvs':
        p = CVSParser()
    elif repo.get_type() == 'svn':
        p = SVNParser()
    elif repo.get_type() == 'git':
        p = GitParser()
    elif repo.get_type() == 'bzr':
        p = BzrParser()
    else:
        printerr(f"Error: Unsupported repository type: {repo.get_type(),}")
        return None

    return p
