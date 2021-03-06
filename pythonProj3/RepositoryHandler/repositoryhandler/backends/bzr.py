# bzr.py
#
# Copyright (C) 2020 K.I.A.Derouiche <kamel.derouiche@gmail.com>
# Copyright (C) 2008 Carlos Garcia Campos <carlosgc@gsyc.escet.urjc.es>
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

import re
import pathlib

from repositoryhandler.Command import Command, CommandError
from repositoryhandler.backends import Repository, \
    RepositoryInvalidWorkingCopy, register_backend
from repositoryhandler.backends.watchers import CHECKOUT, UPDATE, LOG


def get_repository_from_path(path) -> str:
    if pathlib.Path(path).is_file():
        path = pathlib.Path(path).parent

    pattern = re.compile("^[ \t]*(checkout of)?(parent)? branch:(.*)$")
    uri = None

    try:
        cmd = ['bzr', 'info']

        command = Command(cmd, path, env={'LC_ALL': 'C'})
        out = command.run_sync()

        for line in out.splitlines():
            match = pattern.match(line)
            if not match:
                continue

            uri = match.group(3).strip()
            break
    except CommandError:
        raise RepositoryInvalidWorkingCopy('"{}" does not appear to be a Bzr '
                                           'working copy'.format(path))

    if uri is None:
        raise RepositoryInvalidWorkingCopy(
            f'"{path}" does not appear to be a Bzr'
            ' working copy')

    return 'bzr', uri


class BzrRepository(Repository):
    '''Bazar Repository'''

    def __init__(self, uri):
        Repository.__init__(self, uri, 'bzr')

    def _check_uri(self, uri) -> BzrRepository:
        type, repo_uri = get_repository_from_path(uri)
        if not repo_uri.startswith(self.uri):
            raise RepositoryInvalidWorkingCopy(f'"{uri}" does not appear to be a '
                                               'Bzr working copy (expected {self.uri}'
                                               ' but got {repo_uri})')

    def copy(self) -> str:
        return BzrRepository(self.uri)

    def checkout(self, module, rootdir, newdir=None, branch=None, rev=None):
        # branch doesn't make sense here module == branch
        if newdir is not None:
            srcdir = pathlib.Path().joinpath(rootdir, newdir)
        elif newdir == '.':
            srcdir = rootdir
        else:
            srcdir = pathlib.Path().joinpath(rootdir, module)
        if pathlib.Path(srcdir).exists():
            try:
                self.update(srcdir, rev)
                return
            except RepositoryInvalidWorkingCopy:
                # If srcdir is not a valid working copy,
                # continue with the checkout
                pass

        cmd = ['bzr', 'branch', self.uri]

        if newdir is not None:
            cmd.append(newdir)
        else:
            cmd.append(module)

        command = Command(cmd, rootdir)
        self._run_command(command, CHECKOUT)

    def update(self, uri, rev=None):
        self._check_uri(uri)

        #TODO: revision

        cmd = ['bzr', 'pull']

        if pathlib.Path(uri).is_file():
            directory = pathlib.Path(uri).parent
        else:
            directory = uri

        command = Command(cmd, directory)
        self._run_command(command, UPDATE)

    def log(self, uri, rev=None, files=None):
        self._check_uri(uri)

        if pathlib.Path(uri).is_file():
            cwd = pathlib.Path(uri).parent
            files = [pathlib.Path(uri).name]
        elif pathlib.Path(uri).is_dir():
            cwd = uri
            files = ['.']
        else:
            cwd = pathlib.Path.cwd()

        cmd = ['bzr', 'log', '-v']

        #TODO: branch

        if files is not None:
            for file in files:
                cmd.append(file)
        else:
            cmd.append(uri)

        command = Command(cmd, cwd)
        self._run_command(command, LOG)

    def rlog(self, module=None, rev=None, files=None) -> None:
        # TODO: is it supported by bzr???
        return

    def diff(self, uri, branch=None, revs=None, files=None):
        # TODO
        pass

    def blame(self, uri, rev=None, files=None):
        # TODO
        pass

    def get_modules(self) -> list:
        #Not supported by Bzr
        return []

    def get_last_revision(self, uri) -> str:
        self._check_uri(uri)

        cmd = ['bzr', 'revno']

        command = Command(cmd, uri)
        try:
            out = command.run_sync()
        except:
            return None

        if out == "":
            return None

        return out.strip('\n\t ')

register_backend('bzr', BzrRepository)
