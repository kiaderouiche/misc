# cvs.py
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

import pathlib
import re

from repositoryhandler.Command import Command
from repositoryhandler.backends import (Repository,
                                        RepositoryInvalidWorkingCopy,
                                        RepositoryCommandError,
                                        register_backend)
from repositoryhandler.backends.watchers import CHECKOUT, UPDATE, CAT, \
        LOG, DIFF, BLAME, LS

CVSPASS_ERROR_MESSAGE = "^.*: CVS password file .*\.cvspass does "\
                        "not exist - creating a new file$"


def get_repository_from_path(path)-> str:
    # Just in case path is a file
    if not pathlib.Path(path).is_dir():
        path = pathlib.Path(path).parent

    cvsroot = pathlib.Path().joinpath(path, 'CVS', 'Root')

    try:
        uri = open(cvsroot, 'r').read().strip()
    except IOError:
        raise RepositoryInvalidWorkingCopy(f'"{path}" does not appear to be a CVS'
                                           ' working copy')

    return 'cvs', uri


class CVSRepository(Repository):
    '''CVS Repository'''

    def __init__(self, uri):
        Repository.__init__(self, uri, 'cvs')

    def __get_repository_for_path(self, path)-> str:
        if not pathlib.Path(path).is_dir():
            basename = pathlib.Path(path).name
            path = pathlib.Path(path).parent
        else:
            basename = None

        repository = pathlib.Path().joinpath(path, 'CVS', 'Repository')

        try:
            rpath = open(repository, 'r').read().strip()
        except IOError:
            raise RepositoryInvalidWorkingCopy(f'"{path}" does not appear to be a CVS'
                                           ' working copy')

        if basename is not None:
            return pathlib.Path().joinpath(rpath, basename)
        else:
            return rpath

    def _run_command(self, command, type, input=None):
        def error_handler(cmd, error) -> str:
            patt = re.compile(CVSPASS_ERROR_MESSAGE)
            return patt.match(error) is not None

        command.set_error_handler(error_handler)
        Repository._run_command(self, command, type, input)

    def get_uri_for_path(self, path)-> str:
        self._check_srcdir(path)

        rpath = self.__get_repository_for_path(path)

        return pathlib.Path().joinpath(self.uri, rpath)

    def _check_srcdir(self, srcuri):
        # srcuri can be a module, directory or file
        if pathlib.Path(srcuri).is_file():
            srcdir = pathlib.Path(srcuri).parent
        else:
            srcdir = srcuri

        type, uri = get_repository_from_path(srcdir)

        if uri != self.uri:
            raise RepositoryInvalidWorkingCopy('"%s" does not appear to be a '
                                               'CVS working copy '
                                               '(expected %s but got %s)'
                                               % (srcdir, self.uri, uri))

    def copy(self) -> str:
        return CVSRepository(self.uri)

    def checkout(self, uri, rootdir, newdir=None, branch=None, rev=None):
        '''Checkout a module or path from repository

        @param uri: Module or path to check out. When using as a path
            it should be relative to the module being the module name
            the root. modulename/path/to/file
        '''

        # TODO: In CVS branch and rev are incompatible, we should
        # raise an exception if both parameters are provided and
        # use them, it doesn't matter which, when only one is provided.
        if newdir is not None:
            srcdir = pathlib.Path().joinpath(rootdir, newdir)
        elif newdir == '.' or uri == '.':
            srcdir = rootdir
        else:
            srcdir = pathlib.Path().joinpath(rootdir, uri)
        if pathlib.Path(srcdir).exists():
            try:
                self.update(srcdir, rev)
                return
            except RepositoryInvalidWorkingCopy:
                # If srcdir is not a valid working copy,
                # continue with the checkout
                pass

        cmd = ['cvs', '-z3', '-q', '-d', self.uri, 'checkout', '-PN']

        if rev is not None:
            cmd.extend(['-r', rev])

        if newdir is not None:
            cmd.extend(['-d', newdir])

        cmd.append(uri)
        command = Command(cmd, rootdir)
        self._run_command(command, CHECKOUT)

    def update(self, uri, rev=None):
        self._check_srcdir(uri)

        cmd = ['cvs', '-z3', '-q', '-d', self.uri, 'update', '-P', '-d']

        if rev is not None:
            cmd.extend(['-r', rev])

        if pathlib.Path(uri).is_file():
            directory = pathlib.Path(uri).parent
            cmd.append(pathlib.Path(uri).name)
        else:
            directory = uri
            cmd.append('.')

        command = Command(cmd, directory)
        self._run_command(command, UPDATE)

    def cat(self, uri, rev=None):
        self._check_srcdir(uri)

        rpath = self.__get_repository_for_path(uri)

        cmd = ['cvs', '-z3', '-q', '-d', self.uri, 'checkout', '-p']

        if rev is not None:
            cmd.extend(['-r', rev])

        if not pathlib.Path(uri).is_dir():
            directory = pathlib.Path(uri).parent
            cmd.append(pathlib.Path().joinpath(rpath, pathlib.Path(uri).name))
        else:
            directory = uri
            cmd.append(rpath)

        command = Command(cmd, directory)
        self._run_command(command, CAT)

    def log(self, uri, rev=None, files=None):
        self._check_srcdir(uri)

        cmd = ['cvs', '-z3', '-q', '-d', self.uri, 'log']

        if rev is not None:
            cmd.extend(['-r', rev])

        if pathlib.Path(uri).is_file():
            directory = pathlib.Path(uri).parent
        else:
            directory = uri

        if files is not None:
            for file in files:
                cmd.append(file)
        else:
            cmd.append('.')

        command = Command(cmd, directory)
        self._run_command(command, LOG)

    def rlog(self, module, rev=None, files=None):
        '''


        Parameters
        ----------
        module : TYPE
            DESCRIPTION.
        rev : TYPE, optional
            DESCRIPTION. The default is None.
        files : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        '''
        cmd = ['cvs', '-z3', '-q', '-d', self.uri, 'rlog']

        if rev is not None:
            cmd.extend(['-r', rev])

        if files is not None:
            for file in files:
                cmd.append(pathlib.Path().joinpath(module, file))
        else:
            cmd.append(module)

        command = Command(cmd)
        self._run_command(command, LOG)

    def diff(self, uri, branch=None, revs=None, files=None):
        self._check_srcdir(uri)

        cmd = ['cvs', '-z3', '-q', '-d', self.uri, 'diff', '-uN']

        if revs is not None:
            for rev in revs:
                cmd.extend(['-r', rev])

        if pathlib.Path(uri).is_file():
            cwd = pathlib.Path(uri).parent
        else:
            cwd = uri

        if files is not None:
            for file in files:
                cmd.append(file)
        else:
            cmd.append('.')

        command = Command(cmd, cwd)
        # If cvs is successful, it returns a successful status; if there is
        # an error, it prints an error message and returns a failure status.
        # One exception to this is the cvs diff command.  It will return a
        # successful status if it found no differences, or a failure status
        # if there were differences or if there was an error.  Because this
        # behavior provides no good way to detect errors, in the future it
        # is possible that cvs  diff  will be changed to behave like the
        # other cvs commands.
        try:
            self._run_command(command, DIFF)
        except RepositoryCommandError as e:
            if e.returncode != 0 and not e.error:
                pass
            else:
                raise e

    def blame(self, uri, rev=None, files=None, mc=False):
        # In cvs rev already includes the branch info
        # so no need for a branch parameter
        self._check_srcdir(uri)

        cmd = ['cvs', '-z3', '-q', '-d', self.uri, 'annotate']

        if rev is not None:
            cmd.extend(['-r', rev])

        if pathlib.Path(uri).is_file():
            directory = pathlib.Path(uri).parent
            target = pathlib.Path(uri).name
        else:
            directory = uri
            target = '.'

        if files is not None:
            for file in files:
                cmd.append(file)
        else:
            cmd.append(target)

        command = Command(cmd, directory)
        self._run_command(command, BLAME)

    def ls(self, uri, rev=None):
        self._check_srcdir(uri)

        cmd = ['cvs', '-z3', '-q', '-d', self.uri, 'list', '-R']

        if rev is not None:
            cmd.extend(['-r', rev])

        if pathlib.Path(uri).is_file():
            directory = pathlib.Path(uri).parent
        else:
            directory = uri

        # cvs doesn't support listing a file
        cmd.append('.')

        command = Command(cmd, directory)
        self._run_command(command, LS)

    def get_modules(self) -> list:
        #Not supported by CVS
        return []

    def get_last_revision(self, uri) -> int:
        self._check_srcdir(uri)

        if not pathlib.Path(uri).is_file():
            return None

        filename = pathlib.Path(uri).name
        path = pathlib.Path(uri).parent

        cmd = ['cvs', 'status', filename]
        command = Command(cmd, path)
        out = command.run_sync()

        retval = None
        for line in out.splitlines():
            if "Working revision:" in line:
                retval = line.split(":", 1)[1].strip().split()[0]

        return retval

register_backend('cvs', CVSRepository)
